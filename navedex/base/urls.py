from django.urls import path

from navedex.base import views

app_name = 'base'
urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='signup'),
]
