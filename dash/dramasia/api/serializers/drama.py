from django.contrib.auth.models import User
from dramasia.models import Drama, DramaCast, DramaGenre, Genre
from rest_framework import serializers
from dramasia.api.serializers.cast import CastSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class DramaSerializer(serializers.ModelSerializer):

    casts = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    def get_casts(self, obj):
        cast = DramaCast.objects.filter(drama=obj)
        serializer = CastSerializer(cast, many=True)
        return serializer.data

    def get_genre(self, obj):
        cast = DramaGenre.objects.filter(drama=obj)
        serializer = GenreSerializer(cast, many=True)
        return serializer.data

    class Meta:
        model = Drama
        fields = '__all__'