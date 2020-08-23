from django.urls import path, include
from rest_framework.routers import DefaultRouter

from navedex.naver import views

router = DefaultRouter()
router.register('naver', views.NaverModelViewSet)

app_name = 'naver'
urlpatterns = [
    path(r'', include(router.urls)),
]
