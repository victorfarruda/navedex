from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from navedex.base import views

app_name = 'base'
urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('login/', obtain_jwt_token, name='login'),
]
