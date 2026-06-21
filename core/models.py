from django.db import models
from django.contrib.auth.models import User

# List of Ugandan regions and districts for better location specificity
UGANDAN_LOCATIONS = [
    ('Kampala', 'Kampala'),
    ('Gulu', 'Gulu'),
    ('Entebbe', 'Entebbe'),
    ('Jinja', 'Jinja'),
    ('Mbarara', 'Mbarara'),
    ('Masaka', 'Masaka'),
    ('Mbale', 'Mbale'),
    ('Arua', 'Arua'),
    ('Lira', 'Lira'),
    ('Fort Portal', 'Fort Portal'),
    ('Mukono', 'Mukono'),
    ('Soroti', 'Soroti'),
    ('Hoima', 'Hoima'),
    ('Kitgum', 'Kitgum'),
    ('Mubende', 'Mubende'),
    ('Kabale', 'Kabale'),
    ('Kasese', 'Kasese'),
    ('Iganga', 'Iganga'),
    ('Other', 'Other Ugandan Location'),
]

FARMER_TYPES = [
    ('smallholder', 'Smallholder Subsistence Farmer'),
    ('commercial', 'Commercial/Semi-commercial Farmer'),
]

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=255, choices=UGANDAN_LOCATIONS, default='Kampala', db_index=True)
    farmer_type = models.CharField(max_length=50, choices=FARMER_TYPES, default='smallholder')

    class Meta:
        verbose_name_plural = "Farmers"

    def __str__(self):
        return self.user.username

class Farm(models.Model):
    SOIL_TYPES = [
        ('loamy', 'Loamy'),
        ('sandy', 'Sandy'),
        ('clayey', 'Clayey'),
        ('silty', 'Silty'),
    ]
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)  # Unique farm name for login purposes
    size_acres = models.DecimalField(max_digits=5, decimal_places=2)
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES, db_index=True)
    water_source = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Farms"

    def __str__(self):
        return f"{self.name} ({self.farmer.user.username})"

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Managers"

    def __str__(self):
        return f"Manager: {self.user.username}"

class Crop(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    ideal_soil = models.CharField(max_length=20, choices=Farm.SOIL_TYPES)
    planting_season = models.CharField(max_length=50)
    expected_yield_per_acre = models.CharField(max_length=100)
    description = models.TextField()
    factors_favouring = models.TextField(blank=True, help_text="AI-generated factors favoring this crop")
    layman_knowledge = models.TextField(blank=True, help_text="Precise explanation for a layman")
    preferred_regions = models.TextField(blank=True, help_text="Ugandan regions where this crop thrives")
    best_for_farmer_type = models.CharField(max_length=50, choices=FARMER_TYPES, default='smallholder')
    market_potential = models.TextField(blank=True, help_text="Market price insights for this crop in Uganda")
    planting_instructions = models.TextField(blank=True, help_text="Step-by-step planting guide")
    pest_disease_management = models.TextField(blank=True, help_text="Local pest/disease control methods")

    class Meta:
        verbose_name_plural = "Crops"

    def __str__(self):
        return self.name


class Livestock(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    best_regions = models.TextField(blank=True)
    expected_income = models.CharField(max_length=100, blank=True)
    housing_requirements = models.TextField(blank=True)
    feeding_guide = models.TextField(blank=True)
    health_tips = models.TextField(blank=True)
    market_info = models.TextField(blank=True)
    best_for_farmer_type = models.CharField(max_length=50, choices=FARMER_TYPES, default='smallholder')

    class Meta:
        verbose_name_plural = "Livestock"

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ('crop', 'Crop'),
        ('livestock', 'Livestock'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    recommendation_type = models.CharField(max_length=50, choices=RECOMMENDATION_TYPES, default='crop')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, null=True, blank=True)
    fertilizer_info = models.TextField(blank=True)
    pesticide_info = models.TextField(blank=True)
    irrigation_info = models.TextField(blank=True)
    soil_analysis = models.TextField(blank=True, help_text="Soil suitability analysis")
    weather_outlook = models.TextField(blank=True, help_text="Local weather & climate data")
    market_insights = models.TextField(blank=True, help_text="Market price insights for Uganda")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name_plural = "Recommendations"
        ordering = ['-created_at']

    def __str__(self):
        if self.recommendation_type == 'crop' and self.crop:
            return f"Crop Recommendation for {self.farm.name} - {self.crop.name}"
        elif self.recommendation_type == 'livestock' and self.livestock:
            return f"Livestock Recommendation for {self.farm.name} - {self.livestock.name}"
        return f"Recommendation for {self.farm.name}"


class ChatSession(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, default='New Conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} - {self.farmer.user.username}"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'Farmer'),
        ('model', 'FarmDSS Advisor'),
    ]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role}: {self.content[:30]}..."
