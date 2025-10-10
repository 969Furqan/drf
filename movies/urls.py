from django.urls import path
from .api import MovieAPIView

app_name = "Movies"

urlpatterns = [
    path('movies/',MovieAPIView.as_view(), name="movie-api" ),
    path('movies/<int:pk>/',MovieAPIView.as_view(), name="movie-api-detail" ),
]