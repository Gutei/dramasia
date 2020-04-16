from django.contrib.auth.models import User
from dramasia.models import Drama, Cast
from rest_framework import viewsets
from dramasia.api.serializers.cast import CastSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status


class CastViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    http_method_names = ['get', ]

    def list(self, request):
        """
        Use this to get cast list.
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

        return super(CastViewSet, self).list(request)