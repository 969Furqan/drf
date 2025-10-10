from factory import faker
from factory.django import DjangoModelFactory
from movies.models import Movies

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movies
    title = faker.Faker('sentence', nb_words = 4)
    genres = faker.Faker('pylist', nb_elements = 3, variable_nb_elements = True, value_types = ['str'])
    