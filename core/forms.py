from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
import random
from .models import Farmer, Farm, Crop, Recommendation, UGANDAN_LOCATIONS

# Try to import optional models/constants
try:
    from .models import FARMER_TYPES, Livestock
except Exception as e:
    FARMER_TYPES = [('smallholder', 'Smallholder Subsistence Farmer')]
    Livestock = None

class FarmerSignupForm(forms.ModelForm):
    """Signup form that creates both a Django user and a linked Farmer record."""
    password = forms.CharField(widget=forms.PasswordInput(), min_length=4, help_text="At least 4 characters.")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), help_text="Enter the same password again.")
    # Farmer details
    phone_number = forms.CharField(max_length=15, required=False, help_text="Optional")
    location = forms.ChoiceField(choices=UGANDAN_LOCATIONS, required=True)
    # First farm details
    farm_name = forms.CharField(max_length=100, required=True, help_text="This is your unique farm login ID!")
    farm_size_acres = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    farm_soil_type = forms.ChoiceField(choices=Farm.SOIL_TYPES, required=True)
    farm_water_source = forms.CharField(max_length=100, required=True)
    
    # Optional farmer_type field
    try:
        farmer_type = forms.ChoiceField(choices=FARMER_TYPES, initial='smallholder', required=True, help_text="What type of farmer are you?")
    except Exception as e:
        pass

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_farm_name(self):
        farm_name = self.cleaned_data.get('farm_name')
        if Farm.objects.filter(name=farm_name).exists():
            raise ValidationError("This farm name is already taken. Please choose another!")
        return farm_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            suggestions = [
                f"{username}{random.randint(10, 99)}",
                f"{username}_{random.randint(1, 9)}",
                f"farm_{username}"
            ]
            suggestions = [s for s in suggestions if not User.objects.filter(username=s).exists()]
            raise ValidationError(
                f"Username '{username}' is already taken. Try: {', '.join(suggestions)}"
            )
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class FarmerFarmForm(forms.ModelForm):
    """Form for farmers to add a new farm, with unique farm name validation."""
    class Meta:
        model = Farm
        fields = ['name', 'size_acres', 'soil_type', 'water_source']

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if Farm.objects.filter(name__iexact=name).exists():
            raise ValidationError("This farm name is already taken. Please choose another!")
        return name

class FarmerProfileForm(forms.ModelForm):
    """Form to update Farmer profile fields after signup."""
    class Meta:
        model = Farmer
        fields = ['phone_number', 'location']
    
    # Optional: add farmer_type if available
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from .models import FARMER_TYPES
            if hasattr(Farmer, 'farmer_type'):
                self.fields['farmer_type'] = forms.ChoiceField(choices=FARMER_TYPES, required=False)
                self.Meta.fields.append('farmer_type')
        except Exception as e:
            pass

# Custom authentication form that accepts either username OR farm name
class FarmLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username or Farm Name", max_length=255)

# Form for admin to add/edit farms
class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['farmer', 'name', 'size_acres', 'soil_type', 'water_source']

# Form for admin to add/edit recommendations
class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['farm', 'crop', 'fertilizer_info', 'pesticide_info', 'irrigation_info']
    
    # Add optional fields if available
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            optional_fields = ['livestock', 'recommendation_type', 'soil_analysis', 'weather_outlook', 'market_insights']
            for field in optional_fields:
                if hasattr(Recommendation, field):
                    if field == 'recommendation_type':
                        from .models import Recommendation
                        self.fields[field] = forms.ChoiceField(choices=Recommendation.RECOMMENDATION_TYPES, required=False)
                    else:
                        self.fields[field] = forms.CharField(widget=forms.Textarea(), required=False)
                    self.Meta.fields.append(field)
        except Exception as e:
            pass

# Form for crop management
class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'ideal_soil', 'planting_season', 'expected_yield_per_acre', 'description']
    
    # Add optional fields if available
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            optional_fields = ['factors_favouring', 'layman_knowledge', 'preferred_regions', 'best_for_farmer_type', 'market_potential', 'planting_instructions', 'pest_disease_management']
            for field in optional_fields:
                if hasattr(Crop, field):
                    if field == 'best_for_farmer_type':
                        from .models import FARMER_TYPES
                        self.fields[field] = forms.ChoiceField(choices=FARMER_TYPES, required=False)
                    else:
                        self.fields[field] = forms.CharField(widget=forms.Textarea(), required=False)
                    self.Meta.fields.append(field)
        except Exception as e:
            pass
