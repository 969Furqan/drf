from factory import faker
from factory.django import DjangoModelFactory
from ..models import Movies

class MovieFactory(DjangoModelFactory):
    class meta:
        model = Movies
    
    title = faker('sentence', nb_words = 4)
    genres = faker('pylist', nb_elements = 3, variable_nb_elements = True, value_types = ['str'])
    