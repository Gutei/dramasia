from django.contrib.auth.models import User
from dramasia.models import Cast
from rest_framework import serializers

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = '__all__'