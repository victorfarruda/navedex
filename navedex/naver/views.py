import django_filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from navedex.naver.models import Naver
from navedex.naver.serializers import NaverSerializer


class NaverModelViewSet(ModelViewSet):
    serializer_class = NaverSerializer
    permission_classes = (AllowAny,)
    queryset = Naver.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'job_role']

    def get_queryset(self):
        return self.queryset.filter(responsible=self.request.user)
