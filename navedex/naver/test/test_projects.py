from django.http import QueryDict
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from navedex.naver.models import Project, Naver


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
    projects = response.json()
    for project in projects:
        assert project.get('id')
        assert project.get('name')
        assert len(project.values()) == 2
    assert len(projects) == Project.objects.filter(responsible=user).count()


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


def test_can_create_new_project(django_user_model, client, db):
    url = reverse('naver:project-list')
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    naver = mommy.make(Naver, responsible=user)
    data = {
        'name': 'Projeto Bom',
        'navers': [naver.id, ]
    }
    client.login(email='foo@bar.com', password='password')
    response = client.post(url, data=data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    project_response = response.json()

    assert project_response.get('id')
    assert data.get('name') == project_response.get('name')
    assert data.get('navers') == project_response.get('navers')
    assert len(project_response.values()) == 3
    assert Project.objects.count() == 1


def test_can_update_a_project(django_user_model, client, db):
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    django_user_model.objects.create_user(email='bar@foo.com', password='password')

    naver = mommy.make(Naver, responsible=user, _quantity=2)
    project = mommy.make(Project, navers=naver, responsible=user)
    other_naver = mommy.make(Naver, responsible=user)
    data = {
        'name': 'Projeto Bom',
        'navers': [other_naver.id, ]
    }

    url = reverse('naver:project-detail', args=(project.id,))
    response = client.put(url, data=data, content_type='application/json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.login(email='bar@foo.com', password='password')
    response = client.put(url, data=data, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    client.login(email='foo@bar.com', password='password')
    response = client.put(url, data=data, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    project_response = response.json()

    assert project.id == project_response.get('id')
    assert data.get('name') == project_response.get('name')
    assert data.get('navers') == project_response.get('navers')
    assert len(project_response.values()) == 3
    assert Project.objects.count() == 1


def test_can_delete_a_project(django_user_model, client, db):
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    django_user_model.objects.create_user(email='bar@foo.com', password='password')
    project = mommy.make(Project, responsible=user)
    url = reverse('naver:project-detail', args=(project.id,))

    response = client.delete(url, content_type='application/json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.login(email='bar@foo.com', password='password')
    response = client.delete(url, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    client.login(email='foo@bar.com', password='password')
    response = client.delete(url, content_type='application/json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Project.objects.count() == 0


def test_can_retrieve_a_project(django_user_model, client, db):
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    django_user_model.objects.create_user(email='bar@foo.com', password='password')
    navers = mommy.make(Naver, responsible=user, _quantity=2)
    project = mommy.make(Project, navers=navers, responsible=user)
    url = reverse('naver:project-detail', args=(project.id,))

    response = client.get(url, content_type='application/json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.login(email='bar@foo.com', password='password')
    response = client.get(url, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    client.login(email='foo@bar.com', password='password')
    response = client.get(url, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert Project.objects.count() == 1
    assert Naver.objects.count() == 2

    project_response = response.json()
    assert project.name == project_response.get('name')
    assert project.navers.count() == len(project_response.get('navers'))
    for naver in project_response.get('navers'):
        assert naver.get('id')
        assert naver.get('name')
        assert naver.get('birthdate')
        assert naver.get('admission_date')
        assert naver.get('job_role')
        assert len(naver.values()) == 5
