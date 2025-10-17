from typing import Type
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase
from movies.models import UserPreferencesModel
from django.db.models.signals import post_save
User = get_user_model()
@receiver(post_save, get_user_model)
def create_or_update_movie_preferences(sender: ModelBase, instance: User, created: bool, **kwargs) -> None:
    if created:
        UserPreferencesModel.objects.create(user = instance)
    else:
        instance.movie_preferences.save()