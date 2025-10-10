from rest_framework import serializers
from movies.models import Movies

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(label = "id", required = False)
    title = serializers.CharField(max_length=150)
    genres = serializers.ListField(
        child = serializers.CharField(max_length=50),
        allow_empty = True,
        default = list
        )
    
    def create(self, verified_data):
        return Movies.objects.create(**verified_data)
    
    def update(self, instance, verified_data):
        print("verified data \n\n\n")
        print(verified_data)
        instance.title = verified_data.get("title", instance.title)
        instance.save()
        return instance