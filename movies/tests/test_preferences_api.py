import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from factory import SubFactory
from factories import UserFactory

# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     "new_preferences, expected_genre",[
#     ({'genres': 'sci-fi'}, 'sci-fi'),
#     ({'genres': 'drama'}, 'drama'),
#     ({'genres': 'action'}, 'action'),
#     ({'genres': 'action', "actor": 'furqan', 'year':"1776"}, 'action'),]
# )
# def test_add_and_retrieve_preferences_success(new_preferences, expected_genre):
#     user = UserFactory()
#     client = APIClient()
#     preference_url = reverse("Movies:user-preferences", kwargs={'user_id':user.id})
#     response = client.post(
#         preference_url, {
#             'new_preferences':new_preferences
#         }, 
#         format='json'
#     )
#     print(response.json())
#     assert response.status_code in [200, 201]
    
#     response = client.get(preference_url)
#     assert response.status_code == 200
#     print(response.data.keys())
#     assert response.data['preferences']['genres'] in [expected_genre]
    
@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_preferences",[
        ({}),
        ({'genreee':'comedy'})
    ]
)
def test_add_preference_failure(new_preferences):
    user = UserFactory()
    client = APIClient()
    
    preference_url = reverse("Movies:user-preferences", kwargs={'user_id':user.id})
    response = client.post(
        preference_url, {
            'new_preferences':new_preferences
        }, 
        format='json'
    )
    print(response.json())
    assert response.status_code == 400, response.json()