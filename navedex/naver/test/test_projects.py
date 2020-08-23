from django.http import QueryDict
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from navedex.naver.models import Project


def test_can_list_projects_by_user(django_user_model, client, db):
    user1 = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    user2 = django_user_model.objects.create_user(email='bar@foo.com', password='password')
    mommy.make(Project, responsible=user1, _quantity=10)
    mommy.make(Project, responsible=user2, _quantity=10)

    client.login(email='foo@bar.com', password='password')
    is_projects_valid(user1, client)
    client.login(email='bar@foo.com', password='password')
    is_projects_valid(user2, client)
    assert Project.objects.count() == 20


def is_projects_valid(user, client):
    url = reverse('naver:project-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    navers = response.json()
    for naver in navers:
        assert naver.get('id')
        assert naver.get('name')
        assert len(naver.values()) == 2
    assert len(navers) == Project.objects.filter(responsible=user).count()


def test_can_list_projects_and_filter_by_name(client, django_user_model, db):
    search_name = 'Projeto muito bom'
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    mommy.make(Project, responsible=user, _quantity=10)
    mommy.make(Project, responsible=user, name=search_name, _quantity=3)
    query_dict = QueryDict('', mutable=True)
    query_dict['name'] = search_name
    url = '%s?%s' % (reverse('naver:project-list'), query_dict.urlencode())

    client.login(email='foo@bar.com', password='password')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    projects = response.json()
    for project in projects:
        assert project.get('name') == search_name
    assert len(projects) == 3
