from django.urls import path
from .api import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UserPreferenceAPIView, UserWatchHistoryAPIView

app_name = "Movies"

urlpatterns = [
    path('movies/',CreateAPIView.as_view(), name="movie-api" ),
    path('movies/<int:pk>/',RetrieveUpdateDestroyAPIView.as_view(), name="movie-api-detail" ),
    path('movies/all/',ListAPIView.as_view(), name="movie-list-api" ),
    path('user/<int:user_id>/preferences', UserPreferenceAPIView.as_view(), name = 'user-preferences'),
    path('user/<int:user_id>/watch-history', UserWatchHistoryAPIView.as_view(), name = 'user-watch-history'),
]