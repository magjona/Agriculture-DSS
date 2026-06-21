from django.contrib import admin
from .models import Farmer, Farm, Crop, Recommendation

admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(Crop)
admin.site.register(Recommendation)
