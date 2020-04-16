from django.contrib.auth.models import User
from dramasia.models import Drama, DramaCast, DramaGenre, Genre
from rest_framework import serializers
from dramasia.api.serializers.cast import CastSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class DramaCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = DramaCast
        fields = '__all__'

class DramaSerializer(serializers.ModelSerializer):

    casts = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    def get_casts(self, obj):
        cast = DramaCast.objects.filter(drama=obj)
        serializer = DramaCastSerializer(cast, many=True)
        return serializer.data

    def get_genre(self, obj):
        genre = DramaGenre.objects.filter(drama=obj)
        serializer = GenreSerializer(genre, many=True)
        return serializer.data

    class Meta:
        model = Drama
        fields = '__all__'