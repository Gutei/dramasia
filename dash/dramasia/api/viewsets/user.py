from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from dramasia.api.serializers.user import UserSerializer, UserMinimizedSerializer, AuthSerializer, ProfileUserSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework.decorators import (api_view, authentication_classes,
                                       detail_route, list_route,
                                       parser_classes, permission_classes,
                                       renderer_classes, action)

from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from dramasia.models import ProfileUser

from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework import status


class DjangoUserViewSet(viewsets.ModelViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer
    parser_classes = [MultiPartParser,]
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'put']

    def list(self, request):
        """
        Use this to get user list.
        ---
            Header:
                x-token: "xxxxxx"
        """

        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        return super(DjangoUserViewSet, self).list(request)


    def retrieve(self, request, pk=None):
        """
        Use this to get user profile.
        ---
            Header:
                x-token: "xxxxxx"
            --------------------------
            parameter:

            Fill the 'id' parameter with 'profile id'. Not user id.
            You can get the profile id and user id by accessing this endpoint:
            [GET] /nebula/v1/user/profile/get_self_profile/

        """
        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        return super(DjangoUserViewSet, self).retrieve(request)

    def update(self, request, pk):
        """
        Use this to update user's profile.
        ---
            Header:
                x-token: "xxxxxx"
            --------------------------
            parameter:

            Fill the 'id' parameter with 'profile id'. Not user id.
            You can get the profile id and user id by accessing this endpoint:
            [GET] /nebula/v1/user/profile/get_self_profile/

        """

        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        return super(UpdateUserViewSet, self).update(request, pk)

    @action(detail=False, methods=['GET'])
    def get_self_profile(self, request):
        """
        Use this to get logged in user profile.
        ---
            Header:
                x-token: "xxxxxx"
        """

        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN')).first()
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

            profile = ProfileUser.objects.filter(user=valid.user).first()
            if not profile:
                return Response({'message': 'Something wrong. Token is valid but can not find user profile'}, status=HTTP_404_NOT_FOUND)

            serializer = ProfileUserSerializer(profile)

            return Response(serializer.data, status=HTTP_200_OK)

        profile = ProfileUser.objects.filter(user=request.user).first()
        if not profile:
            return Response({'message': 'Something wrong. Token is valid but can not find user profile'}, status=HTTP_404_NOT_FOUND)

        serializer = ProfileUserSerializer(profile)

        return Response(serializer.data, status=HTTP_200_OK)



class UpdateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['put',]

    def update(self, request, pk):
        """
        Use this to update username/password user.
        ---
            Header:
                x-token: "xxxxxx"

            --------------------------
            parameter:

            Fill the 'id' parameter with 'user id'.
            You can get the user id by accessing this endpoint:
            [GET] /nebula/v1/user/profile/get_self_profile/
        """
        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        password = make_password(request.data.get('password'))
        user = get_object_or_404(User, pk=pk)

        super(UpdateUserViewSet, self).update(request, pk)
        user.password = password
        user.username = request.data.get('username')
        try:
            user.save()
        except Exception as e:
            return Response({"messages": "Bad Request"}, status=HTTP_400_BAD_REQUEST)

        return Response({"messages": "Success"}, status=HTTP_200_OK)



class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['post',]

    permission_classes = [AllowAny, ]

    def create(self, request):
        """
        Use this to register new user.
        ---
            Header:
                {} - no need
        """

        cek_username = User.objects.filter(username=request.data.get('username')).first()
        if cek_username:
            return Response({"messages": "Username is exist"}, status=HTTP_400_BAD_REQUEST)

        cek_email = User.objects.filter(username=request.data.get('email')).first()
        if cek_email:
            return Response({"messages": "Email is used"}, status=HTTP_400_BAD_REQUEST)

        a = super(RegisterUserViewSet, self).create(request)
        user = User.objects.filter(username=request.data.get('username')).first()
        if user:
            profile = ProfileUser(user=user)
            profile.save()

        return a