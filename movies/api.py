from django.shortcuts import get_object_or_404
from requests import Request
from rest_framework import views, status
from rest_framework.response import Response

from movies.services import add_preferences, user_preferences, add_watch_history, user_watch_history
from .models import Movies, UserPreferencesModel
from .serializers import AddToWatchHistorySerializer, MovieSerializer, AddPreferenceSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model

User = get_user_model()

class UserWatchHistoryAPIView(generics.RetrieveUpdateAPIView):
    def post(self, request:Request, user_id:int) -> Response:
        serializer = AddToWatchHistorySerializer(data = request.data)
        if serializer.is_valid():
            add_watch_history(
                user_id, 
                serializer.validated_data['id'],
            )
            return Response(
                {'message': "movie added to watch histroy"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def get(self, request:Request, user_id:int) -> Response:
        data = user_watch_history(user_id)
        return Response(data)
            

class UserPreferenceAPIView(generics.RetrieveUpdateAPIView):

    def get(self, request:Request, user_id:int) -> Response:
        data = user_preferences(user_id)
        return Response(data)

    def post(self, request:Request, user_id:int) -> Response:
        serializer = AddPreferenceSerializer(data = request.data)
        if serializer.is_valid():
            add_preferences(user_id, serializer.validated_data["new_preferences"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


        
    
    
class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    
class ListAPIView(generics.ListAPIView):
    queryset = Movies.objects.all().order_by('id')
    serializer_class = MovieSerializer
    
class CreateAPIView(generics.CreateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    

# class MovieAPIView(views.APIView):
#     def post(self, request):
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status = status.HTTP_201_CREATED)
#         return (serializer.errors, status.HTTP_400_BAD_REQUEST)
    
#     def get(self, request, pk = None):
#         if pk:
#             movie = get_object_or_404(Movies, pk = pk)
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#         else:
#             movies = Movies.objects.all()
#             serializer = MovieSerializer(movies, many = True)
#             return Response(
#                 {
#                     "count": len(serializer.data),
#                     "results": serializer.data,
#                     "previous": None,
#                     "next": None
#                 }
#             )
            
#     def put(self, request, pk):
#         movie = get_object_or_404(Movies, pk = pk)
#         print("movie \n\n\n")
#         print(movie.title)
#         print("request\n\n\n")
#         print(request.data)
#         serializer = MovieSerializer(movie, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status = status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         movie = get_object_or_404(Movies, pk = pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)