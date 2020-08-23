from django.db import models
from rest_framework_jwt.serializers import User


class Naver(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    birthdate = models.DateField(null=False, blank=False)
    admission_date = models.DateField(null=False, blank=False)
    job_role = models.CharField(max_length=120, null=False, blank=False)
    responsible = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    responsible = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    navers = models.ManyToManyField(Naver, related_name='projects')

