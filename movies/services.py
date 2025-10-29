from typing import Dict, Any
from collections import defaultdict
from django.db import  transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from movies.models import UserPreferencesModel, Movies
from .serializers import PreferenceSerializer
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
import datetime



def add_preferences(user_id:int, new_preferences:Dict[str, Any]) -> None:
    with transaction.atomic():
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

# upload stuf

import csv
import json
from django.core.exceptions import ValidationError
from typing import Callable
def parse_csv(file_input) -> int:
    movies_processed = 0
    
    # Handle both file paths and InMemoryUploadedFile objects
    if hasattr(file_input, 'read'):
        # It's a file-like object (InMemoryUploadedFile)
        file_input.seek(0)  # Reset file pointer to beginning
        content = file_input.read().decode('utf-8')
        reader = csv.DictReader(content.splitlines())
    else:
        # It's a file path string
        with open(file_input, encoding="utf-8") as file:
            reader = csv.DictReader(file)
    
    for row in reader:
        create_or_update_movie(**row)
        movies_processed += 1
    return movies_processed


def parse_json(file_input) -> int:
    movies_processed = 0
    
    # Handle both file paths and InMemoryUploadedFile objects
    if hasattr(file_input, 'read'):
        # It's a file-like object (InMemoryUploadedFile)
        file_input.seek(0)  # Reset file pointer to beginning
        content = file_input.read().decode('utf-8')
        data = json.loads(content)
    else:
        # It's a file path string
        with open(file_input, encoding="utf-8") as file:
            data = json.load(file)
    
    for item in data:
        create_or_update_movie(**item)
        movies_processed += 1
    return movies_processed
class FileProcessor:
    def process(self, file_name: str, file_type: str) -> int:
        # Check if the file exists in the default storage
        if default_storage.exists(file_name):
        # Open the file directly from storage
            with default_storage.open(file_name, "r") as file:
                if file_type == "text/csv":
                    movies_processed = parse_csv(file)
                elif file_type == "application/json":
                    movies_processed = parse_json(file)
                else:
                    raise ValidationError("Invalid file type")
            return movies_processed
        else:
            raise ValidationError("File does not exist in storage.")
    
    
def create_or_update_movie(
    title:str,
    genres:list,
    country: str | None = None,
    extra_data: dict[Any, Any] | None = None,
    release_year: int | None = None,
):
    try:
        current_year = datetime.datetime.now().year
        if release_year is not None and (release_year < current_year and release_year > 1888):
            raise ValidationError("the release year has to be between 1888 and 2025")
        movie, created = Movies.objects.update_or_create(
            title= title,
            defaults={
                "genres":genres,
                "country":country,
                "extra_data":extra_data,
                "release_year":release_year
            }
        )
        return movie, created
    except Exception as e:
        raise ValidationError(f"failed to create or update the movie {str(e)}")