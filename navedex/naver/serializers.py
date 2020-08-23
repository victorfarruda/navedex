from rest_framework.serializers import ModelSerializer

from navedex.naver.models import Naver


class NaverSerializer(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role',)
        depth = 0


class NaverSerializerPOST(ModelSerializer):
    class Meta:
        model = Naver
        fields = ('id', 'name', 'birthdate', 'admission_date', 'job_role', 'responsible')
        depth = 0
