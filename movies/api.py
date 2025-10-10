from django.shortcuts import get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from .models import Movies
from .serializers import MovieSerializer

class MovieAPIView(views.APIView):
    def post(self, request):
        serializer = MovieSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        return (serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk = None):
        if pk:
            movie = get_object_or_404(Movies, pk = pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        else:
            movies = Movies.objects.all()
            serializer = MovieSerializer(movies, many = True)
            return Response(
                {
                    "count": len(serializer.data),
                    "results": serializer.data,
                    "previous": None,
                    "next": None
                }
            )
            
    def put(self, request, pk):
        movie = get_object_or_404(Movies, pk = pk)
        print("movie \n\n\n")
        print(movie.title)
        print("request\n\n\n")
        print(request.data)
        serializer = MovieSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = get_object_or_404(Movies, pk = pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)