from django.contrib import admin
from .models import UserProfile, Fish, FishCollection

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Fish)
admin.site.register(FishCollection)
