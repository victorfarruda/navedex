from django.http import QueryDict
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from navedex.naver.models import Naver


def test_can_list_navers_by_user(django_user_model, client, db):
    user1 = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    user2 = django_user_model.objects.create_user(email='bar@foo.com', password='password')
    mommy.make(Naver, responsible=user1, _quantity=10)
    mommy.make(Naver, responsible=user2, _quantity=10)

    client.login(email='foo@bar.com', password='password')
    is_navers_valid(user1, client)
    client.login(email='bar@foo.com', password='password')
    is_navers_valid(user2, client)
    assert Naver.objects.count() == 20


def is_navers_valid(user, client):
    url = reverse('naver:naver-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    navers = response.json()
    for naver in navers:
        assert naver.get('id')
        assert naver.get('name')
        assert naver.get('birthdate')
        assert naver.get('admission_date')
        assert naver.get('job_role')
        assert len(naver.values()) == 5
    assert len(navers) == Naver.objects.filter(responsible=user).count()


def test_can_list_navers_and_filter_by_name(client, django_user_model, db):
    search_name = 'Ciclano'
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    mommy.make(Naver, responsible=user, _quantity=10)
    mommy.make(Naver, responsible=user, name=search_name, _quantity=2)
    query_dict = QueryDict('', mutable=True)
    query_dict['name'] = search_name
    url = '%s?%s' % (reverse('naver:naver-list'), query_dict.urlencode())

    client.login(email='foo@bar.com', password='password')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    navers = response.json()
    for naver in navers:
        assert naver.get('name') == search_name
    assert len(navers) == 2


def test_can_list_navers_and_filter_by_job_role(client, django_user_model, db):
    search_job_role = 'Desenvolvedor'
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    mommy.make(Naver, responsible=user, _quantity=10)
    mommy.make(Naver, responsible=user, job_role=search_job_role, _quantity=3)
    query_dict = QueryDict('', mutable=True)
    query_dict['job_role'] = search_job_role
    url = '%s?%s' % (reverse('naver:naver-list'), query_dict.urlencode())

    client.login(email='foo@bar.com', password='password')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    navers = response.json()
    for naver in navers:
        assert naver.get('job_role') == search_job_role
    assert len(navers) == 3


def test_can_create_new_naver(django_user_model, client, db):
    url = reverse('naver:naver-list')
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    data = {
        'name': 'Fulano',
        'birthdate': '1999-05-15',
        'admission_date': '2020-06-12',
        'job_role': 'Desenvolvedor',
        'projects': [],
    }
    client.login(email='foo@bar.com', password='password')
    response = client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    naver_response = response.json()

    assert data.get('name') == naver_response.get('name')
    assert data.get('birthdate') == naver_response.get('birthdate')
    assert data.get('admission_date') == naver_response.get('admission_date')
    assert data.get('job_role') == naver_response.get('job_role')
    assert Naver.objects.count() == 1


def test_can_update_a_naver(django_user_model, client, db):
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    other_user = django_user_model.objects.create_user(email='bar@foo.com', password='password')
    naver = mommy.make(Naver, responsible=user)
    url = reverse('naver:naver-detail', args=(naver.id,))
    data = {
        'name': 'Fulano',
        'birthdate': '1999-05-15',
        'admission_date': '2020-06-12',
        'job_role': 'Desenvolvedor',
        'projects': [],
    }
    response = client.put(url, data=data, content_type='application/json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.login(email='bar@foo.com', password='password')
    response = client.put(url, data=data, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    client.login(email='foo@bar.com', password='password')
    response = client.put(url, data=data, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    naver_response = response.json()

    assert data.get('name') == naver_response.get('name')
    assert data.get('birthdate') == naver_response.get('birthdate')
    assert data.get('admission_date') == naver_response.get('admission_date')
    assert data.get('job_role') == naver_response.get('job_role')
    assert Naver.objects.count() == 1


def test_can_delete_a_naver(django_user_model, client, db):
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    other_user = django_user_model.objects.create_user(email='bar@foo.com', password='password')
    naver = mommy.make(Naver, responsible=user)
    url = reverse('naver:naver-detail', args=(naver.id,))

    response = client.delete(url, content_type='application/json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.login(email='bar@foo.com', password='password')
    response = client.delete(url, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    client.login(email='foo@bar.com', password='password')
    response = client.delete(url, content_type='application/json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Naver.objects.count() == 0


def test_can_retrieve_a_naver(django_user_model, client, db):
    user = django_user_model.objects.create_user(email='foo@bar.com', password='password')
    other_user = django_user_model.objects.create_user(email='bar@foo.com', password='password')
    naver = mommy.make(Naver, responsible=user)
    url = reverse('naver:naver-detail', args=(naver.id,))

    response = client.get(url, content_type='application/json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.login(email='bar@foo.com', password='password')
    response = client.get(url, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    client.login(email='foo@bar.com', password='password')
    response = client.get(url, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert Naver.objects.count() == 1

    naver_response = response.json()
    assert naver.name == naver_response.get('name')
    assert str(naver.birthdate) == naver_response.get('birthdate')
    assert str(naver.admission_date) == naver_response.get('admission_date')
    assert naver.job_role == naver_response.get('job_role')
