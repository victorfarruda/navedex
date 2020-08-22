from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_jwt.serializers import User

from navedex.base.serializers import UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
