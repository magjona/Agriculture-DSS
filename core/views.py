import logging
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Farmer, Farm, Crop, Recommendation, Manager, UGANDAN_LOCATIONS, Livestock, ChatSession, ChatMessage
from .forms import (
    FarmerSignupForm,
    FarmLoginForm,
    FarmForm,
    FarmerFarmForm,
    FarmerProfileForm,
    RecommendationForm,
    CropForm,
)
from .weather_service import get_uganda_weather_data, get_weather_advisory
from .gemini_service import call_gemini_api, generate_ai_recommendations, is_error_response

logger = logging.getLogger(__name__)
def landing(request):
    """Landing page view tailored for Ugandan farmers."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Get weather for user's potential location (default to Kampala for landing page)
    weather = get_uganda_weather_data('Kampala')
    weather_advisory = get_weather_advisory(weather)
    
    return render(request, 'core/landing.html', {
        'weather': weather,
        'weather_advisory': weather_advisory,
        'is_manager': False
    })

def signup(request):
    """Signup form for Ugandan farmers with farm information."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = FarmerSignupForm(request.POST)
        if form.is_valid():
            # Save user
            user = form.save()
            # Save farmer
            farmer_kwargs = {
                'user': user,
                'phone_number': form.cleaned_data.get('phone_number', ''),
                'location': form.cleaned_data['location']
            }
            # Add farmer_type if field exists
            try:
                farmer_kwargs['farmer_type'] = form.cleaned_data.get('farmer_type', 'smallholder')
            except Exception as e:
                logger.warning(f"Farmer type field not available: {e}")
            
            farmer = Farmer.objects.create(**farmer_kwargs)
            # Save first farm
            Farm.objects.create(
                farmer=farmer,
                name=form.cleaned_data['farm_name'],
                size_acres=form.cleaned_data['farm_size_acres'],
                soil_type=form.cleaned_data['farm_soil_type'],
                water_source=form.cleaned_data['farm_water_source']
            )
            # Log the user in
            login(request, user)
            logger.info(f"New farmer registered: {user.username}, Farm: {form.cleaned_data['farm_name']}")
            messages.success(request, "Welcome to Farm Decision Support System! Your farm account has been created.")
            return redirect('dashboard')
    else:
        form = FarmerSignupForm()
    
    return render(request, 'core/signup.html', {
        'form': form,
        'is_manager': False
    })

def custom_login(request):
    """Custom login that accepts both username and farm name."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = FarmLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Try to authenticate with username first
            user = authenticate(username=username, password=password)
            
            # If that fails, try to find a farm with this name and get its user
            if not user:
                try:
                    farm = Farm.objects.get(name=username)
                    user = authenticate(username=farm.farmer.user.username, password=password)
                except Farm.DoesNotExist:
                    user = None
            
            if user:
                login(request, user)
                logger.info(f"User logged in: {user.username}")
                return redirect('dashboard')
        
        messages.error(request, "Invalid farm name/username or password!")
    
    else:
        form = FarmLoginForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required
def dashboard(request):
    """Farmer dashboard view for Uganda-focused recommendations."""
    is_manager = hasattr(request.user, 'manager') or request.user.is_staff
    
    if is_manager:
        return redirect('manager_dashboard')
    
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        farmer = Farmer.objects.create(
            user=request.user,
            location="Kampala"
        )
        logger.info(f"Created farmer profile for user {request.user.username}")

    farms = Farm.objects.filter(farmer=farmer)
    recommendation_qs = Recommendation.objects.filter(
        farm__farmer=farmer
    ).select_related('farm', 'crop').order_by('-created_at')

    paginator = Paginator(recommendation_qs, 10)
    page_number = request.GET.get('page', 1)
    recommendations = paginator.get_page(page_number)
    
    # Get weather data based on farmer's location
    weather = get_uganda_weather_data(farmer.location)
    weather_advisory = get_weather_advisory(weather)
    
    return render(request, 'core/dashboard.html', {
        'farmer': farmer,
        'farms': farms,
        'recommendations': recommendations,
        'weather': weather,
        'weather_advisory': weather_advisory,
        'is_manager': is_manager,
    })

@login_required
def add_farm(request):
    """Add a new farm for an existing farmer."""
    is_manager = hasattr(request.user, 'manager') or request.user.is_staff
    
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        farmer = Farmer.objects.create(user=request.user, location="Kampala")

    if request.method == 'POST':
        form = FarmerFarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = farmer
            farm.save()
            logger.info(f"Added farm '{farm.name}' for user {request.user.username}")
            messages.success(request, f"Farm '{farm.name}' added successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = FarmerFarmForm()

    return render(request, 'core/add_farm.html', {
        'form': form,
        'is_manager': is_manager
    })

@login_required
def edit_profile(request):
    """Edit the current farmer's profile information."""
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        farmer = Farmer.objects.create(user=request.user, location="Kampala")

    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('dashboard')
        messages.error(request, "Please correct the errors in your profile.")
    else:
        form = FarmerProfileForm(instance=farmer)

    return render(request, 'core/edit_profile.html', {
        'form': form,
        'is_manager': False
    })

@login_required
def delete_my_recommendation(request, rec_id):
    """Allow farmers to delete their own recommendations safely via POST."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    farmer = get_object_or_404(Farmer, user=request.user)
    rec = get_object_or_404(Recommendation, id=rec_id, farm__farmer=farmer)
    rec.delete()
    messages.success(request, "Recommendation removed.")
    return redirect('dashboard')
def get_advisor_system_instruction(farmer):
    farms = Farm.objects.filter(farmer=farmer)
    farms_summary = []
    for f in farms:
        farms_summary.append(f"- {f.name}: {f.size_acres} acres, soil: {f.get_soil_type_display()}, water: {f.water_source}")
    farms_text = "\n".join(farms_summary) if farms_summary else "No farms registered yet."

    weather = get_uganda_weather_data(farmer.location)
    weather_text = f"Temp: {weather.get('temperature')}°C, Condition: {weather.get('condition')}, Rain: {weather.get('rainfall')} Rainfall"

    instruction = f"""You are 'AgriAI', the FarmDSS AI Agricultural Advisor, a highly experienced and friendly agricultural expert specializing in Ugandan farming systems.
You provide clear, practical, and layman-friendly advice to Ugandan smallholder farmers.

Farmer Profile Context:
- Location: {farmer.location}
- Farmer Type: {farmer.get_farmer_type_display()}
- Farm Details:
{farms_text}
- Current Weather Context: {weather_text}

Guidelines:
1. Be extremely encouraging, polite, and respectful.
2. Speak in simple, non-jargon English. If asked by the farmer, translate summaries of your advice into Ugandan local languages (like Luganda, Runyankole, Acholi, Swahili).
3. Offer precise step-by-step instructions.
4. Recommend low-cost, organic, and locally-accessible materials (e.g., compost, animal manure, neem leaves, wood ash) for subsistence farmers. Avoid advocating for expensive machinery or inputs unless they identify as a commercial farmer.
5. If recommending a crop, suggest one of the 18 pre-loaded crops supported by FarmDSS if suitable, but feel free to advise on other crops as well.
"""
    return instruction


@login_required
def chat_index(request):
    """Shows a list of the farmer's chat sessions. If none exist, redirects to create one."""
    farmer = get_object_or_404(Farmer, user=request.user)
    sessions = ChatSession.objects.filter(farmer=farmer)
    
    if not sessions.exists():
        session = ChatSession.objects.create(farmer=farmer, title="General Farm Advisory")
        return redirect('chat_session', session_id=session.id)
        
    latest_session = sessions.first()
    return redirect('chat_session', session_id=latest_session.id)


@login_required
def chat_session_view(request, session_id):
    """Renders the chat interface for a specific session and handles sending messages."""
    farmer = get_object_or_404(Farmer, user=request.user)
    session = get_object_or_404(ChatSession, id=session_id, farmer=farmer)
    sessions = ChatSession.objects.filter(farmer=farmer)

    # Bug Fix 1: Eagerly evaluate history BEFORE saving the new message.
    # Using list() forces QuerySet execution NOW so the new user message
    # is NOT included in the history sent to Gemini.
    prior_messages = list(session.messages.all())

    if request.method == 'POST':
        user_text = request.POST.get('message', '').strip()
        if user_text:
            # Save the user message AFTER we have snapshotted prior history
            ChatMessage.objects.create(session=session, role='user', content=user_text)
            session.save()

            # Build history from the snapshot (does NOT include the new message)
            history = [{'role': msg.role, 'content': msg.content} for msg in prior_messages]

            system_instruction = get_advisor_system_instruction(farmer)
            ai_response = call_gemini_api(
                user_text,
                system_instruction=system_instruction,
                chat_history=history,
                timeout=15
            )

            # Bug Fix 2: Only persist a real AI response, never an error string.
            if is_error_response(ai_response):
                logger.warning(f"Gemini returned an error for session {session.id}: {ai_response}")
                messages.error(
                    request,
                    "Musa is temporarily unavailable. Please try again in a moment."
                )
            else:
                ChatMessage.objects.create(session=session, role='model', content=ai_response)
                session.save()

                # Auto-rename session title based on first user message
                if session.title in ['New Conversation', 'General Farm Advisory'] and len(prior_messages) == 0:
                    title_prompt = (
                        f"Summarize this farming question into a short title "
                        f"(max 4 words, plain text only, no quotes): '{user_text}'"
                    )
                    short_title = call_gemini_api(
                        title_prompt,
                        system_instruction="Output only a short title of max 4 words. No punctuation, no quotes."
                    )
                    if short_title and not is_error_response(short_title):
                        session.title = short_title.strip().strip('"').strip("'")[:100]
                        session.save()

            return redirect('chat_session', session_id=session.id)

    # Reload messages fresh for rendering (now includes both sides of any exchange)
    chat_messages = session.messages.all()

    return render(request, 'core/chat_session.html', {
        'farmer': farmer,
        'active_session': session,
        'sessions': sessions,
        'chat_messages': chat_messages,
        'is_manager': False
    })


@login_required
def create_chat_session(request):
    """Creates a new chat session and redirects to it."""
    farmer = get_object_or_404(Farmer, user=request.user)
    session = ChatSession.objects.create(farmer=farmer, title="New Conversation")
    return redirect('chat_session', session_id=session.id)


@login_required
def delete_chat_session(request, session_id):
    """Deletes a chat session."""
    farmer = get_object_or_404(Farmer, user=request.user)
    session = get_object_or_404(ChatSession, id=session_id, farmer=farmer)
    session.delete()
    messages.success(request, "Conversation deleted.")
    return redirect('chat_index')


@login_required
def generate_recommendation(request, farm_id):
    """Generate Uganda-specific AI recommendations for a farm with soil analysis and market insights."""
    is_manager = hasattr(request.user, 'manager') or request.user.is_staff
    
    if is_manager:
        return redirect('manager_dashboard')
    
    try:
        farmer = Farmer.objects.get(user=request.user)
        farm = Farm.objects.get(id=farm_id, farmer=farmer)
    except (Farmer.DoesNotExist, Farm.DoesNotExist):
        logger.warning(f"Farm/farmer not found: {request.user.username}, {farm_id}")
        messages.error(request, "Farm not found!")
        return redirect('dashboard')
    
    weather = get_uganda_weather_data(farmer.location)
    weather_advisory = get_weather_advisory(weather)
    
    # Clear old recommendations first
    Recommendation.objects.filter(farm=farm).delete()
    recommendations_made = 0

    # Try Gemini AI recommendations first if key is configured
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if api_key:
        logger.info("Attempting to generate recommendations via Gemini API")
        ai_recs = generate_ai_recommendations(farm, weather, weather_advisory)
        if ai_recs:
            for item in ai_recs:
                crop_name = item.get('crop_name')
                if not crop_name:
                    continue
                try:
                    crop = Crop.objects.get(name__iexact=crop_name)
                except Crop.DoesNotExist:
                    crop = Crop.objects.filter(name__icontains=crop_name).first()
                    if not crop:
                        logger.warning(f"AI recommended crop '{crop_name}' not found in database.")
                        continue

                score = item.get('confidence_score', 75)
                evidence = item.get('evidence', [])
                if isinstance(evidence, list):
                    evidence_str = " | ".join(evidence)
                else:
                    evidence_str = str(evidence)

                try:
                    rec_kwargs = {
                        'farm': farm,
                        'crop': crop,
                        'fertilizer_info': f"Confidence: {'HIGH' if score >= 75 else 'MEDIUM'} ({score}%)\nEvidence: {evidence_str}\n\nFertilizer Guide: {item.get('fertilizer_info', '')}",
                        'pesticide_info': item.get('pesticide_info', ''),
                        'irrigation_info': item.get('irrigation_info', ''),
                    }
                    if hasattr(Recommendation, 'recommendation_type'):
                        rec_kwargs['recommendation_type'] = 'crop'
                    if hasattr(Recommendation, 'soil_analysis'):
                        rec_kwargs['soil_analysis'] = item.get('soil_analysis', '')
                    if hasattr(Recommendation, 'weather_outlook'):
                        rec_kwargs['weather_outlook'] = item.get('weather_outlook', f"Current: {weather.get('condition')}, {weather.get('temperature', weather.get('temp', 25))}°C\nOutlook: {item.get('weather_outlook', '')}")
                    if hasattr(Recommendation, 'market_insights'):
                        rec_kwargs['market_insights'] = item.get('market_insights', '')

                    Recommendation.objects.create(**rec_kwargs)
                    recommendations_made += 1
                except Exception as e:
                    logger.warning(f"Could not create AI recommendation for {crop_name}: {e}")

            # Also generate livestock recommendations (standard rule-based)
            try:
                all_livestock = Livestock.objects.all()
                for livestock in all_livestock:
                    # Apply farmer-specific filtering
                    if hasattr(livestock, 'best_for_farmer_type') and livestock.best_for_farmer_type != farmer.farmer_type:
                        continue
                    if farm.size_acres < 1 and any(large_animal in livestock.name.lower() for large_animal in ['cattle', 'cow', 'dairy']):
                        continue
                    if hasattr(livestock, 'best_regions') and livestock.best_regions:
                        regions = livestock.best_regions.lower()
                        if 'all' not in regions and farmer.location.lower() not in regions:
                            continue

                    try:
                        rec_kwargs = {
                            'farm': farm,
                            'livestock': livestock,
                            'recommendation_type': 'livestock',
                            'fertilizer_info': f"Potential: {livestock.name} for income",
                            'pesticide_info': livestock.health_tips or "Good husbandry practices recommended." if hasattr(livestock, 'health_tips') else "Good husbandry practices recommended.",
                            'irrigation_info': f"Housing: {livestock.housing_requirements}\nFeeding: {livestock.feeding_guide}" if hasattr(livestock, 'housing_requirements') else "",
                        }
                        if hasattr(Recommendation, 'market_insights') and hasattr(livestock, 'market_info'):
                            rec_kwargs['market_insights'] = livestock.market_info or "Good market potential."
                        Recommendation.objects.create(**rec_kwargs)
                        recommendations_made += 1
                    except Exception as e:
                        logger.warning(f"Could not create livestock recommendation: {e}")
            except Exception as e:
                logger.warning(f"Livestock model not available: {e}")

            if recommendations_made > 0:
                logger.info(f"Generated {recommendations_made} AI recommendations for farm {farm.name}")
                messages.success(request, f"Successfully generated {recommendations_made} tailored AI recommendations using Gemini!")
                return redirect('dashboard')
            else:
                logger.warning("Gemini AI failed to produce valid recommendations. Falling back to rule-based recommendations.")
        else:
            logger.warning("Gemini AI recommendation call failed. Falling back to rule-based recommendations.")

    # FALLBACK RULE-BASED SCORER (Original Logic)
    logger.info("Running fallback rule-based recommendation generator")
    all_crops = Crop.objects.all()
    target_crops = all_crops
    try:
        if hasattr(farmer, 'farmer_type') and farmer.farmer_type:
            target_crops = all_crops.filter(best_for_farmer_type=farmer.farmer_type)
    except Exception as e:
        logger.warning(f"Farmer type field not available: {e}")
    
    for crop in target_crops:
        score = 0
        evidence = []
        
        # Soil match (40%)
        soil_analysis_text = ""
        if crop.ideal_soil == farm.soil_type:
            score += 40
            evidence.append(f"✓ Your {farm.get_soil_type_display()} soil is PERFECT for {crop.name}!")
            soil_analysis_text = f"Excellent soil match! {crop.name} thrives in {farm.get_soil_type_display()} soil."
        else:
            score += 10
            evidence.append(f"○ {crop.name} prefers {crop.get_ideal_soil_display()} soil, but can grow with care.")
            soil_analysis_text = f"Can grow in {farm.get_soil_type_display()} soil with amendments."
        
        # Water/season (30%)
        water_source_lower = farm.water_source.lower()
        planting_season_lower = crop.planting_season.lower()
        
        if ('rain' in water_source_lower and 
            ('rain' in planting_season_lower or 'march' in planting_season_lower or 'august' in planting_season_lower or 'september' in planting_season_lower)):
            score += 30
            evidence.append(f"✓ Perfect rainfall alignment!")
        elif ('irrigation' in water_source_lower or 'well' in water_source_lower or 'borehole' in water_source_lower):
            score += 25
            evidence.append(f"○ Your {farm.water_source} provides stable water.")
        
        # Weather (20%)
        weather_outlook_text = f"Current: {weather.get('condition')}, {weather.get('temperature', weather.get('temp', 25))}°C"
        if (weather.get('rainfall') == 'heavy' and ('rainy' in planting_season_lower or 'march' in planting_season_lower)):
            score += 20
            evidence.append(f"✓ Current weather is ideal for {crop.name}!")
        
        # Location match (10%)
        try:
            if hasattr(crop, 'preferred_regions') and crop.preferred_regions and farm.farmer.location.lower() in crop.preferred_regions.lower():
                score += 10
                evidence.append(f"✓ {crop.name} thrives in {farm.farmer.location}!")
        except Exception as e:
            logger.warning(f"Preferred regions field not available: {e}")
        
        # If we have a decent score, make the recommendation
        try:
            rec_kwargs = {
                'farm': farm,
                'crop': crop,
                'fertilizer_info': f"Confidence: {'HIGH' if score >=75 else 'MEDIUM'} ({score}%)\nEvidence: {' | '.join(evidence)}",
                'pesticide_info': crop.layman_knowledge or "Follow standard protection guidelines." if hasattr(crop, 'layman_knowledge') else "Follow standard protection guidelines.",
                'irrigation_info': f"Strategy: {weather['forecast']}\nBased on {farm.water_source} and current {weather['condition']}.",
            }
            if hasattr(Recommendation, 'recommendation_type'):
                rec_kwargs['recommendation_type'] = 'crop'
            if hasattr(Recommendation, 'soil_analysis'):
                rec_kwargs['soil_analysis'] = soil_analysis_text
            if hasattr(Recommendation, 'weather_outlook'):
                rec_kwargs['weather_outlook'] = weather_outlook_text
            if hasattr(Recommendation, 'market_insights') and hasattr(crop, 'market_potential'):
                rec_kwargs['market_insights'] = crop.market_potential or "Good market demand in Uganda."
            if hasattr(crop, 'planting_instructions') and crop.planting_instructions:
                rec_kwargs['irrigation_info'] += f"\nPlanting Guide: {crop.planting_instructions}"
            if hasattr(crop, 'pest_disease_management') and crop.pest_disease_management:
                rec_kwargs['pesticide_info'] = crop.pest_disease_management
            
            if score >= 50:
                Recommendation.objects.create(**rec_kwargs)
                recommendations_made += 1
        except Exception as e:
            logger.warning(f"Could not create recommendation: {e}")
    
    # Also add livestock recommendations if applicable
    try:
        all_livestock = Livestock.objects.all()
        for livestock in all_livestock:
            # Apply farmer-specific filtering
            if hasattr(livestock, 'best_for_farmer_type') and livestock.best_for_farmer_type != farmer.farmer_type:
                continue
            if farm.size_acres < 1 and any(large_animal in livestock.name.lower() for large_animal in ['cattle', 'cow', 'dairy']):
                continue
            if hasattr(livestock, 'best_regions') and livestock.best_regions:
                regions = livestock.best_regions.lower()
                if 'all' not in regions and farmer.location.lower() not in regions:
                    continue

            try:
                rec_kwargs = {
                    'farm': farm,
                    'livestock': livestock,
                    'recommendation_type': 'livestock',
                    'fertilizer_info': f"Potential: {livestock.name} for income",
                    'pesticide_info': livestock.health_tips or "Good husbandry practices recommended." if hasattr(livestock, 'health_tips') else "Good husbandry practices recommended.",
                    'irrigation_info': f"Housing: {livestock.housing_requirements}\nFeeding: {livestock.feeding_guide}" if hasattr(livestock, 'housing_requirements') else "",
                }
                if hasattr(Recommendation, 'market_insights') and hasattr(livestock, 'market_info'):
                    rec_kwargs['market_insights'] = livestock.market_info or "Good market potential."
                Recommendation.objects.create(**rec_kwargs)
                recommendations_made += 1
            except Exception as e:
                logger.warning(f"Could not create livestock recommendation: {e}")
    except Exception as e:
        logger.warning(f"Livestock model not available: {e}")
    
    if recommendations_made > 0:
        logger.info(f"Generated {recommendations_made} recommendations for farm {farm.name}")
        messages.success(request, f"Successfully generated {recommendations_made} tailored recommendations!")
    else:
        messages.warning(request, "No high-confidence matches found. Try adding more crops!")
    
    return redirect('dashboard')

@staff_member_required
def manager_dashboard(request):
    """Admin dashboard to manage farms, crops, livestock, and recommendations."""
    crops = Crop.objects.all()
    livestock = []
    try:
        from .models import Livestock
        livestock = Livestock.objects.all()
    except Exception as e:
        logger.warning(f"Livestock model not available: {e}")
    
    farmers = Farmer.objects.select_related('user').all()
    farms = Farm.objects.select_related('farmer__user').all()
    try:
        recommendations = Recommendation.objects.select_related('farm', 'crop').all()
        # Try to add livestock to select_related if available
        if hasattr(Recommendation, 'livestock'):
            recommendations = Recommendation.objects.select_related('farm', 'crop', 'livestock').all()
    except Exception as e:
        recommendations = Recommendation.objects.select_related('farm', 'crop').all()
    
    # Group recommendations by location
    recommendations_by_location = {}
    weather_by_location = {}
    for rec in recommendations:
        loc = rec.farm.farmer.location
        if loc not in recommendations_by_location:
            recommendations_by_location[loc] = []
            weather_by_location[loc] = get_uganda_weather_data(loc)
        recommendations_by_location[loc].append(rec)
    
    return render(request, 'core/manager_dashboard.html', {
        'crops': crops,
        'livestock': livestock,
        'farmers': farmers,
        'farms': farms,
        'recommendations': recommendations,
        'recommendations_by_location': recommendations_by_location,
        'weather_by_location': weather_by_location,
        'is_manager': True
    })

@staff_member_required
def edit_farm(request, farm_id=None):
    """Add or edit a farm (admin only)."""
    farm = None
    if farm_id:
        farm = get_object_or_404(Farm, id=farm_id)
    
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            action = "updated" if farm else "created"
            logger.info(f"Farm {action}: {form.cleaned_data['name']}")
            messages.success(request, f"Farm successfully {action}!")
            return redirect('manager_dashboard')
    else:
        form = FarmForm(instance=farm)
    
    return render(request, 'core/edit_farm.html', {
        'form': form,
        'farm': farm,
        'is_manager': True
    })

@staff_member_required
def delete_farm(request, farm_id):
    """Delete a farm (admin only)."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    farm = get_object_or_404(Farm, id=farm_id)
    farm_name = farm.name
    farm.delete()
    logger.info(f"Deleted farm: {farm_name}")
    messages.success(request, f"Farm '{farm_name}' deleted successfully!")
    return redirect('manager_dashboard')

@staff_member_required
def edit_crop(request, crop_id=None):
    """Add or edit a crop (admin only)."""
    crop = None
    if crop_id:
        crop = get_object_or_404(Crop, id=crop_id)
    
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            action = "updated" if crop else "created"
            logger.info(f"Crop {action}: {form.cleaned_data['name']}")
            messages.success(request, f"Crop successfully {action}!")
            return redirect('manager_dashboard')
    else:
        form = CropForm(instance=crop)
    
    return render(request, 'core/edit_crop.html', {
        'form': form,
        'crop': crop,
        'is_manager': True
    })

@staff_member_required
def delete_crop(request, crop_id):
    """Delete a crop (admin only)."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    crop = get_object_or_404(Crop, id=crop_id)
    crop_name = crop.name
    crop.delete()
    logger.info(f"Deleted crop: {crop_name}")
    messages.success(request, f"Crop '{crop_name}' deleted successfully!")
    return redirect('manager_dashboard')

@staff_member_required
def edit_recommendation(request, rec_id=None):
    """Add or edit a recommendation (admin only)."""
    recommendation = None
    if rec_id:
        recommendation = get_object_or_404(Recommendation, id=rec_id)
    
    if request.method == 'POST':
        form = RecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            form.save()
            action = "updated" if recommendation else "created"
            logger.info(f"Recommendation {action}!")
            messages.success(request, f"Recommendation successfully {action}!")
            return redirect('manager_dashboard')
    else:
        form = RecommendationForm(instance=recommendation)
    
    return render(request, 'core/edit_recommendation.html', {
        'form': form,
        'recommendation': recommendation,
        'is_manager': True
    })

@staff_member_required
def delete_recommendation(request, rec_id):
    """Delete a recommendation (admin only)."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    rec = get_object_or_404(Recommendation, id=rec_id)
    rec.delete()
    logger.info(f"Deleted recommendation!")
    messages.success(request, "Recommendation deleted successfully!")
    return redirect('manager_dashboard')
