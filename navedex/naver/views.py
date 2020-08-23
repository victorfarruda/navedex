import django_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from navedex.naver.models import Naver, Project
from navedex.naver import serializers


class NaverModelViewSet(ModelViewSet):
    serializer_class = serializers.NaverSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Naver.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'job_role']

    def get_queryset(self):
        return self.queryset.filter(responsible=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return serializers.NaverSerializerPostOrPut(*args, **kwargs)
        elif self.request.method == 'GET' and not kwargs.get('many'):
            return serializers.NaverSerializerGet(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)

    def create(self, *args, **kwargs):
        self.request.data['responsible'] = self.request.user.id
        return super().create(self.request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.request.data['responsible'] = self.request.user.id
        return super().update(self.request, *args, **kwargs)


class ProjectModelViewSet(ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name']

    def get_queryset(self):
        return self.queryset.filter(responsible=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return serializers.ProjectSerializerPostOrPut(*args, **kwargs)
        elif self.request.method == 'GET' and not kwargs.get('many'):
            return serializers.ProjectSerializerGet(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)

    def create(self, *args, **kwargs):
        self.request.data['responsible'] = self.request.user.id
        return super().create(self.request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.request.data['responsible'] = self.request.user.id
        return super().update(self.request, *args, **kwargs)
