from django.contrib.auth.models import User
from dramasia.models import Drama, DramaCast, DramaGenre, Genre
from rest_framework import serializers
from dramasia.api.serializers.cast import CastSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'genre')

class DramaOnlyGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DramaGenre
        fields = ('genre',)

class DramaCastSerializer(serializers.ModelSerializer):

    cast = CastSerializer()

    class Meta:
        model = DramaCast
        exclude = ('id', 'drama',)

class DramaSerializer(serializers.ModelSerializer):

    casts = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    def get_casts(self, obj):
        cast = DramaCast.objects.filter(drama=obj)
        serializer = DramaCastSerializer(cast, many=True)
        return serializer.data

    def get_genre(self, obj):
        genre = DramaGenre.objects.filter(drama=obj)
        serializer = DramaOnlyGenreSerializer(genre, many=True)
        return serializer.data

    class Meta:
        model = Drama
        fields = '__all__'


class DramaGenreSerializer(serializers.ModelSerializer):
    drama = serializers.SerializerMethodField()
    # genre = serializers.SerializerMethodField()

    def get_drama(self, obj):
        drama = obj.drama
        serializer = DramaSerializer(drama)
        return serializer.data

    # def get_genre(self, obj):
    #     genre = obj.genre
    #     serializer = GenreSerializer(genre)
    #     return serializer.data

    class Meta:
        model = DramaGenre
        fields = ('drama',)
