from typing import Dict, Any
from collections import defaultdict
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from movies.models import UserPreferencesModel, Movies
from .serializers import PreferenceSerializer, WatchHistorySerializer

def add_preferences(user_id:int, new_preferences:Dict[str, Any]) -> None:
    with transaction.Atomic():
        user = get_object_or_404(get_user_model(),id = user_id)
        (user_preferences, created) = UserPreferencesModel.objects.select_for_update().get_or_create( user_id = user.id, defaults = {'preferences':{}})
        
        current_preferences = defaultdict(list, user_preferences.preferences)
        for key, value in new_preferences.items():
            if value not in current_preferences[key]:
                current_preferences[key].append(value)
        user_preferences.preferences = dict(current_preferences)
        user_preferences.save()
        
def add_watch_history(user_id: int, movie_id: int) -> None:

    movie = get_object_or_404(Movies, id=movie_id)
    movie_info = {
    "title": movie.title,
    "year": movie.release_year,
    "director": movie.extra_data.get("directors", []),
    "genre": movie.genres,
    }
   
    with transaction.atomic():
        user_preferences, created = UserPreferencesModel.objects.get_or_create(
            user_id=user_id, defaults={"watch_history": [movie_info]}
        )

    
        if not created:
            current_watch_history = user_preferences.watch_history or []
            
            if not any(m['title'] == movie_info['title'] for m in current_watch_history):
            # Add new movie info to existing watch history
                current_watch_history = user_preferences.watch_history
                current_watch_history.append(movie_info)
                user_preferences.watch_history = current_watch_history
                user_preferences.save()
            
def user_preferences(user_id: int) -> Any:
    user_preferences = get_object_or_404(UserPreferencesModel,
    user_id=user_id)
    serializer = PreferenceSerializer(user_preferences.preferences)
    return serializer.data

def user_watch_history(user_id: int) -> dict[str, Any]:
    user_preferences = get_object_or_404(UserPreferencesModel,
    user_id=user_id)
    return {"watch_history": user_preferences.watch_history}