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
from dramasia.api.serializers.user import UserSerializer, UserMinimizedSerializer, AuthSerializer
from rest_framework import viewsets
from rest_framework.decorators import (api_view, authentication_classes,
                                       detail_route, list_route,
                                       parser_classes, permission_classes,
                                       renderer_classes)

from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post',]

    def create(self, request):
        """
        Use this to request token.
        ---
            Header:
                {} - no need
        """
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=HTTP_200_OK)
