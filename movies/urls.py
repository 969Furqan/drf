from django.urls import path
from .api import RetrieveUpdateDestroyAPIView, MovieListCreateAPIView, UserPreferenceAPIView, UserWatchHistoryAPIView, GeneralUploadView

app_name = "Movies"

urlpatterns = [
    path('movies/',MovieListCreateAPIView.as_view(), name="movie-api" ),
    path('movies/<int:pk>/',RetrieveUpdateDestroyAPIView.as_view(), name="movie-api-detail" ),
    path('user/<int:user_id>/preferences/', UserPreferenceAPIView.as_view(), name = 'user-preferences'),
    path('user/<int:user_id>/watch-history/', UserWatchHistoryAPIView.as_view(), name = 'user-watch-history'),
    path('upload', GeneralUploadView.as_view(), name ="upload_movie")
]