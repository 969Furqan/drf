import pytest

from movies.serializers import MovieSerializer
from movies.models import Movies


@pytest.mark.django_db
def test_valid_movie_serializer():
    valid_data = {
        "title": "inception",
        "genres": [
            "sci-fi", "fantasy"
        ]
    }
    serializer = MovieSerializer(data = valid_data)
    assert serializer.is_valid()
    serializer.save()
    assert Movies.objects.count() == 1
    created_movie = Movies.objects.get()
    assert created_movie.title == valid_data["title"]
    assert created_movie.genres == valid_data["genres"]
    
@pytest.mark.django_db
def test_invalid_movie_serializer():
    invalid_data = {
        "genres": [
            "sci-fi", "fantasy"
        ],
    }
    serializer = MovieSerializer(data = invalid_data)
    
    assert not serializer.is_valid()
    assert "title" in serializer.errors
    
    
@pytest.mark.django_db
def test_serialize_model_instance():
    new_movie = Movies.objects.create(
        title = "inception",
        genres = ["action", "sci-fi"]
        )
    
    serializer = MovieSerializer(new_movie)
    assert serializer.data == {
        "id": new_movie.id,
        "title": new_movie.title,
        "genres": new_movie.genres
    }
    
    



