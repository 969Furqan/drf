from datetime import date, datetime
from rest_framework import serializers
from movies.models import Movies, UserPreferencesModel
from rest_framework.validators import UniqueTogetherValidator

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'title', 'genres', 'country', 'extra_data', 'release_year']
        validators = [
            UniqueTogetherValidator(
                queryset= Movies.objects.all(),
                fields = ['title', 'genres']
            )
        ]
    
    def create(self, verified_data):
        return Movies.objects.create(**verified_data)
    
    def update(self, instance, verified_data):
        instance.title = verified_data.get("title", instance.title)
        instance.save()
        return instance
    


class PreferenceDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPreferencesModel
        fields = '__all__'
    genre = serializers.CharField(max_length = 100, allow_blank = True, required = False)
    directors = serializers.CharField(max_length = 100, allow_blank = True, required = False)
    actor = serializers.CharField  (max_length = 100, allow_blank = True, required = False)
    year = serializers.IntegerField(min_value = 1950, max_value = datetime.now().year, required = False)
    
    def validate(self, data = [str, any]) -> dict[str, any]:
        if all(value in [None, ""] for value in data.values()):
            raise serializers.ValidationError("At least one preference must be provided.")
        return data
class AddPreferenceSerializer(serializers.Serializer):
    new_preferences = PreferenceDetailSerializer()
    
class PreferenceSerializer(serializers.Serializer):
    
    genre = serializers.ListField(child = serializers.CharField(), required = False)
    directors = serializers.ListField(child = serializers.CharField(), required = False)
    actor = serializers.ListField(child = serializers.CharField(), required = False)
    year = serializers.ListField(child = serializers.CharField(), required = False)
    
class AddToWatchHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
    def Validate(self, value:int) -> int:
        if not Movies.objects.filter(id = value).exists():
            raise serializers.ValidationError("movie does not exist")
        return value
    
class WatchHistorySerializer(serializers.Serializer):
    title = serializers.ListField(child = serializers.CharField(), required = False)
    directors = serializers.ListField(child = serializers.CharField(), required = False)
    genre = serializers.ListField(child = serializers.CharField(), required = False)
    year = serializers.ListField(child = serializers.CharField(), required = False)