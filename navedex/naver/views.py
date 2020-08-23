import django_filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from navedex.naver.models import Naver
from navedex.naver.serializers import NaverSerializer, NaverSerializerPOST


class NaverModelViewSet(ModelViewSet):
    serializer_class = NaverSerializer
    permission_classes = (AllowAny,)
    queryset = Naver.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'job_role']

    def get_queryset(self):
        return self.queryset.filter(responsible=self.request.user)

    def get_serializer(self, data, *args, **kwargs):
        if self.request.method == 'POST':
            return NaverSerializerPOST(data=data)
        return self.serializer_class(data=data)

    def create(self, request, *args, **kwargs):
        self.request.data._mutable = True
        self.request.data.appendlist('responsible', self.request.user.id)
        self.request.data._mutable = False
        return super().create(self.request, *args, **kwargs)
