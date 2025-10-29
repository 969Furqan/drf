from requests import Request
from rest_framework import status
from rest_framework.response import Response

from movies.tasks import process_file
from .models import Movies
from .serializers import AddToWatchHistorySerializer, MovieSerializer, AddPreferenceSerializer
from rest_framework import generics
from movies.services import add_preferences, user_preferences, add_watch_history, user_watch_history
from django.contrib.auth import get_user_model
from contextlib import contextmanager
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from typing import Any
from movies.serializers import UploadSerializer
from movies.services import FileProcessor
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api_auth.permissions import CustomModelPermissions
from rest_framework.decorators import permission_classes
User = get_user_model()
# @permission_classes([IsAuthenticated])
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
            

# @permission_classes([IsAuthenticated])
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
    
class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movies.objects.all().order_by('id')
    serializer_class = MovieSerializer
    # permission_classes = [IsAuthenticated, CustomModelPermissions]
    
    

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



@contextmanager
def temp_upload(uploaded_file):
    try:
        file_name = default_storage.save(uploaded_file.name, uploaded_file)
        file_path = default_storage.path(file_name)
        yield file_path
    finally:
        default_storage.delete(file_name)

# @permission_classes([IsAdminUser]) 
class GeneralUploadView(APIView):
    def post(self, request, *args:Any, **kwargs: Any) -> Response:
        serializer = UploadSerializer(data = request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            uploaded_file = serializer.validated_data["file"]
            file_type = uploaded_file.content_type
            
            # For CSV files, process directly for immediate feedback
            if file_type == "text/csv":
                try:
                    from .services import parse_csv
                    movies_processed = parse_csv(uploaded_file)
                    return Response(
                        {"message": f"Successfully processed {movies_processed} movies."},
                        status = status.HTTP_202_ACCEPTED
                    )
                except Exception as e:
                    return Response(
                        {"error": f"Failed to process CSV file: {str(e)}"},
                        status = status.HTTP_400_BAD_REQUEST
                    )
            else:
                # For other file types, use Celery background processing
                with temp_upload(uploaded_file) as file_path:
                    process_file.delay(file_path, file_type)
                    return Response(
                        {"message":f"your file is being processed."},
                        status = status.HTTP_202_ACCEPTED
                    )
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                
