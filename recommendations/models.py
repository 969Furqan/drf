from django.db import models

# Create your models here.
class Item(models.Model):
    id: int
    attribute: dict
    
class userPreferences(models.Model):
    preferences: dict | None = None
    watch_history: list[int] | None = []
    