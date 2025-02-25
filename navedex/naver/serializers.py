from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from navedex.naver.models import Naver, Project


class NaverSerializer(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role')
        depth = 0


class NaverSerializerPostOrPut(ModelSerializer):
    projects = PrimaryKeyRelatedField(many=True, read_only=False, queryset=Project.objects.all())

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role', 'responsible', 'projects',)
        extra_kwargs = {'responsible': {'write_only': True}}
        depth = 0


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name',)
        depth = 0


class NaverSerializerGet(ModelSerializer):
    projects = ProjectSerializer(many=True)

    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role', 'projects',)
        depth = 1


class ProjectSerializerPostOrPut(ModelSerializer):
    navers = PrimaryKeyRelatedField(many=True, read_only=False, queryset=Naver.objects.all())

    class Meta:
        model = Project
        fields = ('id', 'name', 'navers', 'responsible',)
        extra_kwargs = {'responsible': {'write_only': True}}
        depth = 0


class ProjectSerializerGet(ModelSerializer):
    navers = NaverSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'navers')
        depth = 1
