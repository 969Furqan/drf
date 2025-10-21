import json
from django.urls import reverse
from rest_framework import status
from movies.models import Movies
import pytest
from django.test import override_settings
from factories import MovieFactory


@pytest.mark.django_db
def test_create_movie(client):
    url = reverse('Movies:movie-api')
    data = {
        'title': 'A New Hope',
        'genres': ['drama', 'adventure'],
    }
    
    response = client.post(url, data = json.dumps(data), content_type = 'application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Movies.objects.filter(title = 'A New Hope').count() == 1
    
    
@pytest.mark.django_db
def test_retrieve_movie(client):
    movie = MovieFactory()
    url = reverse('Movies:movie-api-detail', kwargs={
        'pk':movie.id
    })
    
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK

    assert ('id', movie.id) in response.json().items()
    assert ('title', movie.title) in response.json().items()
    assert ('genres', movie.genres) in response.json().items()

    
@pytest.mark.django_db
def test_update_movie(client):
    movie = MovieFactory()
    url = reverse('Movies:movie-api-detail', kwargs={
        'pk':movie.id
    })
    new_title = 'the new title'
    data = {'title':new_title}
    
    response = client.put(url, data = data, content_type = 'application/json')
    assert response.status_code == status.HTTP_200_OK, response.json
    Movies.objects.filter(id = movie.id).first()
    assert movie
    movie.refresh_from_db()
    assert movie.title == new_title
    

@pytest.mark.django_db
def test_delete_movie(client):
    movie = MovieFactory()
    url = reverse('Movies:movie-api-detail', 
                  kwargs={
                      'pk':movie.id
                  })
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Movies.objects.filter(id = movie.id).exists()
    



@pytest.mark.django_db
@override_settings(REST_FRAMEWORK={'PAGE_SIZE':10})
def test_list_movie(client):
    movies = MovieFactory.create_batch(10)
    url = reverse('Movies:movie-api')
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert 'count' in data
    assert 'previous' in data
    assert 'next' in data
    assert 'results' in data
    
    assert data['count'] == 10
    returned_data = {movie['id'] for movie in data['results']}
    expected_data = {movie.id for movie in movies}
    
    assert returned_data == expected_data
    
    for movie in data['results']:
        print(set(movie.keys()) )
        # assert 'id', 'title', 'genres' in set(movie.keys()) 
        assert all(key in movie for key in {'id', 'title', 'genres'})

    


