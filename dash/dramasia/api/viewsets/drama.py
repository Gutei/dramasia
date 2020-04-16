from django.contrib.auth.models import User
from dramasia.models import Drama
from rest_framework import viewsets
from dramasia.api.serializers.drama import DramaSerializer

class DramaViewSet(viewsets.ModelViewSet):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer
    http_method_names = ['get', ]

    def list(self, request):
        """
        Use this to get drama list.
        ---
            Header:
                - Authorization: "Token xxxxxx"
        """
        return super(DramaViewSet, self).list(request)