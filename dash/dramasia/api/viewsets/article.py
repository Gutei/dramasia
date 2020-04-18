from django.contrib.auth.models import User
from dramasia.models import Drama, Cast, Article
from rest_framework import viewsets
from dramasia.api.serializers.article import ArticleSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_publish=True).order_by('-updated')
    serializer_class = ArticleSerializer
    http_method_names = ['get', ]

    def list(self, request):
        """
        Use this to get cast list.
        ---
            Header:
                x-token: "xxxxxx"

            ------------------------
            For the pagination, You can freely limit content. but by default, this will limit 15 items.
            Use the 'limit' parameter or (?limit=...) in querystring to initiate limit number you want.

            This will automatically give the 'next' attribute that contains the uri to go to the next page
            if the content exceeds the limit.
        """

        if not request.user.is_superuser:

            if not request.META.get('HTTP_X_TOKEN'):
                return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            valid = Token.objects.filter(key=request.META.get('HTTP_X_TOKEN'))
            if not valid:
                return Response({'message': 'Token is not valid.'}, status=status.HTTP_403_FORBIDDEN)

        return super(ArticleViewSet, self).list(request)


    def retrieve(self, request, pk=None):
        """
        Use this to get cast (actress or actors) detail.
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

        return super(ArticleViewSet, self).retrieve(request)