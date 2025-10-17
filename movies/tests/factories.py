from django.contrib.auth.models import User
from factory import faker, SubFactory
from factory.django import DjangoModelFactory
from movies.models import Movies, UserPreferencesModel

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movies
    title = faker.Faker('sentence', nb_words = 4)
    genres = faker.Faker('pylist', nb_elements = 3, variable_nb_elements = True, value_types = ['str'])

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = faker.Faker('user_name')
    
    