from typing import IO, Dict, Any
from collections import defaultdict
from django.db import  transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from movies.models import UserPreferencesModel, Movies
from .serializers import PreferenceSerializer
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
import datetime
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



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
import io
from django.core.exceptions import ValidationError
from typing import Callable
def parse_csv(file_input: IO[Any]) -> int:
    movies_processed = 0
    # Normalize to a text IO for csv module
    if hasattr(file_input, "read"):
        try:
            file_input.seek(0)
        except Exception:
            pass
        content = file_input.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
        text_io = io.StringIO(content)
    else:
        with open(file_input, encoding="utf-8") as f:
            content = f.read()
        text_io = io.StringIO(content)

    reader = csv.DictReader(text_io)

    for row in reader:
        extra_data = row.get("extra_data", "")
        try:
            extra_data_dict = json.loads(extra_data) if isinstance(extra_data, str) else {}
        except json.decoder.JSONDecodeError:
            extra_data_dict = {}
        row["extra_data"] = extra_data_dict
        # Normalize release_year: treat missing/blank as None
        year_raw = row.get("release_year", "")
        if isinstance(year_raw, str):
            year_raw = year_raw.strip()
        if year_raw in ("", None, 0, "0"):
            row["release_year"] = None
        else:
            try:
                row["release_year"] = int(year_raw)
            except (ValueError, TypeError):
                row["release_year"] = None
        row["title"] = clean_text(row.get("title", ""))
        genres_value = row.get("genres", "")
        if isinstance(genres_value, str):
            row["genres"] = [clean_text(genre) for genre in genres_value.split(",") if genre]
        elif isinstance(genres_value, list):
            row["genres"] = [clean_text(genre) for genre in genres_value]
        else:
            row["genres"] = []
        row["country"] = clean_text(row.get("country", ""))
        create_or_update_movie(**row)
        movies_processed += 1
    return movies_processed
            
    # if hasattr(file_input, 'read'):
    #     # It's a file-like object (InMemoryUploadedFile)
    #     file_input.seek(0)  # Reset file pointer to beginning
    #     content = file_input.read().decode('utf-8')
    #     reader = csv.DictReader(content.splitlines())
    # else:
    #     # It's a file path string
    #     with open(file_input, encoding="utf-8") as file:
    #         reader = csv.DictReader(file)
    
    # for row in reader:
    #     create_or_update_movie(**row)
    #     movies_processed += 1
    # return movies_processed


def parse_json(file_input) -> int:
    movies_processed = 0

    # Handle both file paths and file-like objects
    if hasattr(file_input, "read"):
        try:
            file_input.seek(0)
        except Exception:
            pass
        raw_content = file_input.read()
        content = raw_content.decode("utf-8") if isinstance(raw_content, (bytes, bytearray)) else raw_content
        data = json.loads(content)
    else:
        with open(file_input, encoding="utf-8") as file:
            data = json.load(file)

    for item in data:
        # Normalize fields similar to CSV path
        item["title"] = clean_text(item.get("title", ""))
        genres_value = item.get("genres", [])
        if isinstance(genres_value, str):
            item["genres"] = [clean_text(g) for g in genres_value.split(",") if g]
        elif isinstance(genres_value, list):
            item["genres"] = [clean_text(g) for g in genres_value]
        item["country"] = clean_text(item.get("country", ""))
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
        if release_year is not None:
            if not (1888 <= int(release_year) <= current_year):
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
    
def detect_q_string(text: str) -> list:
    pattern = r'Q\d+'
    return re.findall(pattern, text)

def clean_text(text:str)->str:
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    try:
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
        return ' '.join(words)
    except LookupError:
        # Fallback if NLTK data is not available in the environment
        return re.sub(r'\s+', ' ', text).strip()