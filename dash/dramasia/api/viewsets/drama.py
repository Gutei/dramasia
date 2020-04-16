from django.contrib.auth.models import User
from dramasia.models import Drama, Genre, DramaGenre
from rest_framework import viewsets
from dramasia.api.serializers.drama import DramaSerializer, GenreSerializer, DramaGenreSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination)

class DramaViewSet(viewsets.ModelViewSet):
    queryset = Drama.objects.filter(is_publish=True).order_by('-updated')
    serializer_class = DramaSerializer
    http_method_names = ['get', ]

    def list(self, request):
        """
        Use this to get drama list.
        ---
            Header:
                x-token: "xxxxxx"

            ------------------------
            For the pagination, You can freely limit content. but by default, this will limit 15 items.
            Use the 'limit' parameter or (?limit=...) in querystring to initiate limit number you want.

            This will automatically give the 'next' attribute that contains the uri to go to the next page
            if the content exceeds the limit.

            :return

            Example:

            {
              "count": 31,
              "next": "http://139.99.40.74:8000/nebula/v1/drama/?limit=15&offset=15",
              "previous": null,
              "results": [
                {...},
                {...},
                ...
               ]
            }
        """
        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        return super(DramaViewSet, self).list(request)



    def retrieve(self, request, pk=None):
        """
        Use this to get drama detail.
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

        return super(DramaViewSet, self).retrieve(request)




class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('genre')
    serializer_class = GenreSerializer
    http_method_names = ['get', ]

    def list(self, request):
        """
        Use this to get genre list.
        ---
            Header:
                x-token: "xxxxxx"
        """
        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message':'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        return super(GenreViewSet, self).list(request)



    def retrieve(self, request, pk=None):
        """
        Use this to get all dramas those contain this genre.
        ---
            Header:
                x-token: "xxxxxx"
            ------------------------
            returns:

            This will returns Drama objects

            [
                {
                    "drama" : {...}
                }
            ]

            And with the pagination

            {
              "count": 5,
              "next": null,
              "previous": null,
              "results": [
                {
                  "drama": {...}
                }
              ]
            }
        """
        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        genre = Genre.objects.filter(id=pk).first()
        drama_genre = DramaGenre.objects.filter(genre=genre)

        page = self.paginate_queryset(drama_genre)
        serializer = DramaGenreSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)