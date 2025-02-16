import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestAuth:
    def test_signup_success(self, api_client):
        signup_data = {
            "username": "JIN HO",
            "password": "12341234",
            "nickname": "Mentos"
        }

        response = api_client.post('/accounts/signup', signup_data)

        assert response.status_code == 201
        assert response.data['username'] == signup_data['username']
        assert response.data['nickname'] == signup_data['nickname']
        assert response.data['roles'][0] == {'role': 'USER'}

    def test_signup_existing_username(self, api_client):
        User.objects.create_user(
            username="JIN HO", password="12341234", nickname="Mentos")

        response = api_client.post('/accounts/signup', {
            "username": "JIN HO",
            "password": "12341234",
            "nickname": "Mentoster"
        })

        assert response.status_code == 400

    def test_signup_existing_nickname(self, api_client):
        User.objects.create_user(
            username="JIN HOHO", password="12341234", nickname="Mentos")

        response = api_client.post('/accounts/signup', {
            "username": "JIN HO",
            "password": "12341234",
            "nickname": "Mentos"
        })

        assert response.status_code == 400

    def test_signup_empty_data(self, api_client):
        signup_data = {
            "username": "",
            "password": "",
            "nickname": ""
        }

        response = api_client.post('/accounts/signup', signup_data)

        assert response.status_code == 400

    def test_signup_invalid_password(self, api_client):
        signup_data = {
            "username": "JIN HO",
            "password": "1234",
            "nickname": "Mentos"
        }

        response = api_client.post('/accounts/signup', signup_data)
        assert response.status_code == 400

    def test_signup_password_validation(self, api_client):
        response = api_client.post('/accounts/signup', {
            "username": "testuser1",
            "password": "123",
            "nickname": "Test User 1"
        })
        assert response.status_code == 400
        assert 'password' in response.data

        response = api_client.post('/accounts/signup', {
            "username": "testuser4",
            "password": "12345678",  
            "nickname": "Test User 4"
        })
        assert response.status_code == 201  

        response = api_client.post('/accounts/signup', {
            "username": "testuser5",
            "password": "password123",  
            "nickname": "Test User 5"
        })
        assert response.status_code == 201  

    def test_login_success(self, api_client):
        User.objects.create_user(
            username="JIN HO",
            password="12341234",
            nickname="Mentos"
        )

        response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "12341234"
        })

        assert response.status_code == 200
        assert 'token' in response.data

    def test_login_wrong_password(self, api_client):
        User.objects.create_user(
            username="JIN HO",
            password="12341234",
            nickname="Mentos"
        )

        response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "1234123"
        })

        assert response.status_code == 401
        assert 'error' in response.data

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "12341234"
        })

        assert response.status_code == 401
        assert 'error' in response.data

    def test_login_invalid_data(self, api_client):
        response = api_client.post('/accounts/login', {
            "username": "",
            "password": ""
        })

        assert response.status_code == 400
        assert 'error' in response.data

    def test_access_refresh_senario(self, api_client):
        signup_response = api_client.post('/accounts/signup', {
            "username": "JIN HO",
            "password": "12341234",
            "nickname": "Mentos"
        })
        assert signup_response.status_code == 201
        assert User.objects.filter(username="JIN HO").exists()

        login_response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "12341234"
        })
        assert login_response.status_code == 200
        assert 'token' in login_response.data
        refresh_token = login_response.headers.get('X-Refresh-Token')
        assert refresh_token is not None

        refresh_response = api_client.post('/accounts/refresh', 
            headers={'X-Refresh-Token': refresh_token}
        )
        assert refresh_response.status_code == 200
        assert 'token' in refresh_response.data

    def test_invalid_refresh_token(self, api_client):
        response = api_client.post('/accounts/refresh', 
            headers={'X-Refresh-Token': 'invalid_token'}
        )
        assert response.status_code == 401

    def test_missing_refresh_token(self, api_client):
        response = api_client.post('/accounts/refresh')
        assert response.status_code == 400
        assert 'error' in response.data

    def test_expired_refresh_token(self, api_client):
        User.objects.create_user(
            username="JIN HO",
            password="12341234",
            nickname="mentos"
        )

        response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "12341234"
        })
        refresh_token = response.headers.get('X-Refresh-Token')

        response = api_client.post('/accounts/refresh',
            headers={'X-Refresh-Token': refresh_token + "expired"}
        )
        assert response.status_code == 401

    def test_multiple_refresh_attempts(self, api_client):
        User.objects.create_user(
            username="JIN HO",
            password="12341234",
            nickname="mentos"
        )

        response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "12341234"
        })
        refresh_token = response.headers.get('X-Refresh-Token')

        first_refresh = api_client.post('/accounts/refresh',
            headers={'X-Refresh-Token': refresh_token}
        )
        assert first_refresh.status_code == 200
        assert 'token' in first_refresh.data

        second_refresh = api_client.post('/accounts/refresh',
            headers={'X-Refresh-Token': refresh_token}
        )
        assert second_refresh.status_code == 200
        assert 'token' in second_refresh.data

        assert first_refresh.data['token'] != second_refresh.data['token']