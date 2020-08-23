from rest_framework.serializers import ModelSerializer

from navedex.naver.models import Naver


class NaverSerializer(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role')
        write_only_fields = ('responsible',)
        depth = 0


class NaverSerializerGET(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role',)
        depth = 2
