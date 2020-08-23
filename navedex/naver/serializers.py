from rest_framework.serializers import ModelSerializer

from navedex.naver.models import Naver, Project


class NaverSerializer(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role')
        depth = 0


class NaverSerializerPostOrPut(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role', 'responsible')
        write_only_fields = ('responsible',)
        depth = 0


class NaverSerializerGet(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role')
        depth = 2


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name',)
        depth = 0
