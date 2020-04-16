from django.contrib.auth.models import User
from dramasia.models import Drama, Cast
from rest_framework import viewsets
from dramasia.api.serializers.cast import CastSerializer

class CastViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    http_method_names = ['get', ]

    def list(self, request):
        """
        Use this to get cast list.
        ---
            Header:
                - Authorization: "Token xxxxxx"
        """
        return super(CastViewSet, self).list(request)