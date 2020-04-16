from django.contrib.auth.models import User
from dramasia.models import Drama
from rest_framework import viewsets
from dramasia.api.serializers.drama import DramaSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

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