from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from rest_framework.validators import UniqueTogetherValidator

from django.conf import settings

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=500)
    genres = models.JSONField(default=list)
    country = models.CharField(max_length=500, null=True, blank= True)
    extra_data = models.JSONField(default=dict)
    directors = models.JSONField(default=list)
    release_year = models.IntegerField(
        validators=[
            MinValueValidator(1888),
            MaxValueValidator(datetime.now().year)
        ],
        blank=True,
        null=True
    )
    

    def __str__(self):
        return self.title

class UserPreferencesModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_preferences")
    preferences = models.JSONField(default=dict, help_text= "these are the preferencees for the user")
    watch_history = models.JSONField(default=dict, help_text="a field for all that is watched")
    
    def __str__(self):
        return f"{self.user.username}"  