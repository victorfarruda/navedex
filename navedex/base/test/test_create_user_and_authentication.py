from django.urls import reverse
from rest_framework_jwt.serializers import User


def test_can_create_new_user(client, db):
    url = reverse('base:signup')
    email_used = 'my_email@email.com'
    password_used = 'my_password'
    data = {
        'email': email_used,
        'password': password_used,
    }
    client.post(url, data=data)

    assert User.objects.count() == 1
    user_created = User.objects.first()
    assert user_created.email == email_used
    assert user_created.password != password_used


def test_receive_jwt_when_pass_email_and_password(client, db):
    url = reverse('base:login')
    email_used = 'my_email@email.com'
    password_used = 'my_password'
    User.objects.create_user(email=email_used, password=password_used)
    data = {
        'email': email_used,
        'password': password_used,
    }
    response = client.post(url, data=data)
    assert response.json().get('token')
