import json
from django.urls import reverse
from rest_framework import status
from ..models import Movies
import pytest
# Create your tests here.

from .factories import MovieFactory

@pytest.mark.django.db
def test_create_movie(client):
    url = reverse('Movies:movie-api')
    data = {
        "title": "A New Hope",
        "genres": json.dump(["drama", "adventure"])
    }
    
    response = client.post(url, json = data)
    assert response.status_code == status.HTTP_201_CREATED,response.json()
    assert Movies.object.filter(title = "A New Hope").count() == 1
