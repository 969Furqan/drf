import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from factories import UserFactory, MovieFactory
@pytest.mark.django_db
def test_add_and_retrieve_watch_history_with_movie_id() -> None:
    user = UserFactory()
    client = APIClient()
    watch_history_url = reverse("Movies:user-watch-history", kwargs={"user_id":
        user.id})
    # Create movie instances using the MovieFactory
    movie1 = MovieFactory(title="The Godfather", release_year=1972, directors=["Francis Ford Coppola"], genres=["Crime", "Drama"])
    movie2 = MovieFactory(title="Taxi Driver", release_year=1976, directors=["Martin Scorsese"], genres=["Crime", "Drama"])
 # Add movies to watch history using their IDs
    for movie in [movie1, movie2]:
        response = client.post(watch_history_url, {"id": movie.id},
        format="json")
        assert response.status_code == 201
 # Retrieve watch history to verify the addition
    response = client.get(watch_history_url)
    assert response.status_code == 200
 # This assumes your response includes the movie IDs in the watch history
    retrieved_movie_ids = [item["title"] for item in
    response.data["watch_history"]]
    for movie_title in [movie1.title, movie2.title]:
        assert movie_title in retrieved_movie_ids
        
        

@pytest.mark.django_db
def test_add_invalid_movie_id_to_watch_history() -> None:
# Arrange: Create a user instance using Factory Boy
    user = UserFactory()
    client = APIClient()
    watch_history_url = reverse("Movies:user-watch-history", kwargs={"user_id":
        user.id})
    invalid_movie_id = 99999  # Assuming this ID does not exist in the database
    response = client.post(watch_history_url, {"movie_id":
    invalid_movie_id}, format="json")
 # Assert: Check for a 400 Bad Request response
    assert response.status_code == 400, "Expected a 400 Bad Request response for an invalid movie ID"