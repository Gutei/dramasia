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
                                       renderer_classes)

from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from dramasia.models import ProfileUser

from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser


class DjangoUserViewSet(viewsets.ModelViewSet):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer
    parser_classes = [MultiPartParser,]
    http_method_names = ['get', 'put']

    def update(self, request, pk):
        """
        Use this to update user's profile.
        ---
            Header:
                - Authorization: "Token xxxxxx"
        """

        return super(UpdateUserViewSet, self).update(request, pk)



class UpdateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSerializer
    http_method_names = ['put',]

    def update(self, request, pk):
        """
        Use this to update username/password user.
        ---
            Header:
                - Authorization: "Token xxxxxx"
        """
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
        a = super(RegisterUserViewSet, self).create(request)
        user = User.objects.filter(username=request.data.get('username')).first()
        if user:
            profile = ProfileUser(user=user)
            profile.save()

        return a