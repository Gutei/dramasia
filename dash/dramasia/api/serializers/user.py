from django.contrib.auth.models import User
from rest_framework import serializers
from dramasia.models import ProfileUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # fields = '__all__'

class UserMinimizedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions',)

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileUserSerializer(serializers.ModelSerializer):

    id_profile = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        data = {
            'id_user': user.id,
            'username': user.username,
            'email': user.email,
        }
        return data

    def get_id_profile(self, obj):
        user = obj.id
        return user

    class Meta:
        model = ProfileUser
        exclude = ('id',)


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)