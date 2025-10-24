from django.contrib import admin

# Register your models here.
from .models import Movies, UserPreferencesModel

admin.site.register(Movies)
admin.site.register(UserPreferencesModel)
