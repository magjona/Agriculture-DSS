import json
import logging
import time
import requests
from django.conf import settings
from .models import Crop
import urllib3
import datetime
if not getattr(settings, 'VERIFY_SSL', True):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# Strings that indicate an error response (not real AI content)
ERROR_PREFIXES = (
    "Error:", "System Warning:", "The request timed out.",
    "An unexpected error", "I received an unexpected", "I experienced"
)


def is_error_response(text):
    """Returns True if the response text is an error/warning string, not real AI content."""
    if not text:
        return True
    return any(text.strip().startswith(prefix) for prefix in ERROR_PREFIXES)


def _do_post(url, headers, payload, timeout, verify_ssl):
    """Execute a single POST to the Gemini API and return (success, text_or_error)."""
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout, verify=verify_ssl)
        if response.status_code == 200:
            data = response.json()
            try:
                text = data['candidates'][0]['content']['parts'][0]['text']
                return True, text
            except (KeyError, IndexError) as e:
                logger.error(f"Gemini parse error: {e}. Raw: {response.text[:300]}")
                return False, f"Error: Could not parse Gemini response."
        elif response.status_code in (429, 503):
            # Retryable: rate limit or temporary unavailability
            logger.warning(f"Gemini {response.status_code} — will retry. Body: {response.text[:200]}")
            return None, f"retry:{response.status_code}"
        else:
            logger.error(f"Gemini API {response.status_code}: {response.text[:300]}")
            return False, f"Error: Gemini API returned status code {response.status_code}."
    except requests.exceptions.Timeout:
        logger.warning("Gemini API request timed out — will retry.")
        return None, "retry:timeout"
    except Exception as e:
        logger.error(f"Unexpected Gemini error: {str(e)}")
        return False, f"Error: Unexpected error communicating with the AI service."


def call_gemini_api(prompt, system_instruction=None, chat_history=None, timeout=15):
    """
    Calls the Gemini API generateContent endpoint.

    Implements:
      - Configurable timeout (default 15s, pass 30 for heavy prompts)
      - Exponential-backoff retry (up to GEMINI_MAX_RETRIES) on 429/503/timeout
      - Automatic fallback to GEMINI_FALLBACK_MODEL if all retries fail

    Args:
        prompt (str): The user query or task.
        system_instruction (str, optional): System persona/context instructions.
        chat_history (list, optional): Prior messages [{'role': ..., 'content': ...}].
        timeout (int): HTTP request timeout in seconds.

    Returns:
        str: AI text response, or a user-friendly error string.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        logger.warning("Gemini API key is not configured.")
        return "System Warning: Gemini API Key is not set. Please add GEMINI_API_KEY to your .env file."

    primary_model = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash-lite')
    fallback_model = getattr(settings, 'GEMINI_FALLBACK_MODEL', 'gemini-3.0-flash')
    max_retries = getattr(settings, 'GEMINI_MAX_RETRIES', 3)
    verify_ssl = getattr(settings, 'VERIFY_SSL', True)
    headers = {'Content-Type': 'application/json'}

    # Build contents payload
    contents = []
    if chat_history:
        for msg in chat_history:
            role = 'user' if msg.get('role') == 'user' else 'model'
            contents.append({"role": role, "parts": [{"text": msg.get('content', '')}]})

    contents.append({"role": "user", "parts": [{"text": prompt}]})

    payload: dict = {"contents": contents}
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    # Try primary model first, then fallback
    for model_name in [primary_model, fallback_model]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        logger.info(f"Calling Gemini model: {model_name}")

        for attempt in range(1, max_retries + 1):
            success, result = _do_post(url, headers, payload, timeout, verify_ssl)

            if success is True:
                logger.info(f"Gemini success on model={model_name}, attempt={attempt}")
                return result

            if success is False:
                # Non-retryable error — try fallback model next
                logger.warning(f"Non-retryable error on {model_name}: {result}")
                break

            # success is None → retryable; exponential backoff
            wait = 2 ** (attempt - 1)  # 1s, 2s, 4s
            logger.info(f"Retry {attempt}/{max_retries} for {model_name} in {wait}s…")
            time.sleep(wait)

        logger.warning(f"All {max_retries} attempts exhausted for model {model_name}. Trying next model.")

    logger.error("All Gemini models failed. Returning error to caller.")
    return "Error: The AI service is temporarily unavailable. Please try again in a moment."


def generate_ai_recommendations(farm, weather, weather_advisory):
    """
    Leverages Gemini to analyse farm conditions and return structured crop recommendations.

    Uses a lightweight, compact prompt (only essential crop fields) and a longer timeout
    to accommodate the free-tier latency.

    Returns:
        list[dict] | None: Recommendation objects, or None on failure.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return None

    # Compact crop catalog — only the fields needed for matching
    crops = Crop.objects.all().values('name', 'ideal_soil', 'planting_season', 'preferred_regions')
    crops_compact = [
        {
            "name": c['name'],
            "ideal_soil": c['ideal_soil'],
            "planting_season": c['planting_season'],
            "regions": c['preferred_regions'] or "all Uganda",
        }
        for c in crops
    ]

    prompt = f"""You are an expert Ugandan agricultural advisor. Analyse this farm and return crop recommendations as a JSON array.

FARM:
- Location: {farm.farmer.location}
- Farmer Type: {farm.farmer.get_farmer_type_display() if hasattr(farm.farmer, 'get_farmer_type_display') else farm.farmer.farmer_type}
- Soil: {farm.soil_type}
- Water: {farm.water_source}
- Size: {farm.size_acres} acres

WEATHER & SEASON:
- Current Month: {datetime.date.today().strftime('%B')} (Consider this for planting windows)
- Temp: {weather.get('temperature')}°C, Condition: {weather.get('condition')}, Rainfall: {weather.get('rainfall')}
- Advisory: {weather_advisory}

AVAILABLE CROPS (choose only from this list):
{json.dumps(crops_compact, indent=2)}

Rank the crops by the absolute best fit for THIS specific farmer's size, farmer type, and the current weather/season.

Return ONLY a valid JSON array (no markdown, no extra text) with 3-6 crops. Each item must have:
- crop_name (string, exact name from list)
- confidence_score (integer 0-100)
- evidence (string, 1-2 sentences why it fits)
- fertilizer_info (string, practical local advice)
- pesticide_info (string, local pest/disease tips)
- irrigation_info (string, water management advice)
- soil_analysis (string, soil compatibility note)
- weather_outlook (string, weather suitability note)
- market_insights (string, Ugandan market/price insight)
"""

    system_instruction = "You only output valid JSON arrays. No markdown, no prose, no code fences."

    try:
        # Use a longer timeout for this larger prompt
        response_text = call_gemini_api(prompt, system_instruction=system_instruction, timeout=30)

        if is_error_response(response_text):
            logger.warning(f"Gemini recommendation call returned an error: {response_text}")
            return None

        # Strip markdown fences if model added them despite instructions
        cleaned = response_text.strip()
        for fence in ("```json", "```"):
            if cleaned.startswith(fence):
                cleaned = cleaned[len(fence):]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        recommendations = json.loads(cleaned)
        if isinstance(recommendations, list) and len(recommendations) > 0:
            logger.info(f"Gemini returned {len(recommendations)} crop recommendations.")
            return recommendations

        logger.warning("Gemini returned an empty or non-list JSON for recommendations.")
        return None

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error parsing Gemini recommendations: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in generate_ai_recommendations: {e}")
        return None
