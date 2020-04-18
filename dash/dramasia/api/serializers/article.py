from django.contrib.auth.models import User
from dramasia.models import Drama, DramaCast, DramaGenre, Genre, Article
from rest_framework import serializers
from dramasia.api.serializers.cast import CastSerializer


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'