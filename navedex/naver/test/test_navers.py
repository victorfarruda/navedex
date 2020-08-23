from django.http import QueryDict
from django.urls import reverse
from model_mommy import mommy

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
    assert response.status_code == 200
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
    assert response.status_code == 200
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
    assert response.status_code == 200
    navers = response.json()
    for naver in navers:
        assert naver.get('job_role') == search_job_role
    assert len(navers) == 3
