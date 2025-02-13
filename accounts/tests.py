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
        # Given: 회원가입 데이터 준비
        signup_data = {
            "username": "JIN HO",
            "password": "12341234",
            "nickname": "Mentos"
        }
        
        # When: 회원가입 요청
        response = api_client.post('/accounts/signup', signup_data)
        
        # Then: 응답 검증
        assert response.status_code == 201
        assert response.data['username'] == signup_data['username']
        assert response.data['nickname'] == signup_data['nickname']
        assert response.data['roles'][0] == {'role': 'USER'}
    
    def test_signup_existing_username(self, api_client):
        # Given: 이미 존재하는 사용자
        User.objects.create_user(username="JIN HO", password="12341234", nickname="Mentos")
        
        # When: 같은 username으로 회원가입 시도
        response = api_client.post('/accounts/signup', {
            "username": "JIN HO",
            "password": "12341234",
            "nickname": "Mentoster"
        })
        
        # Then: 에러 응답 검증
        assert response.status_code == 400


    def test_signup_existing_nickname(self, api_client):
        # Given: 이미 존재하는 사용자
        User.objects.create_user(username="JIN HOHO", password="12341234", nickname="Mentos")
        
        # When: 같은 nickname으로 회원가입 시도
        response = api_client.post('/accounts/signup', {
            "username": "JIN HO",
            "password": "12341234",
            "nickname": "Mentos"
        })
        
        # Then: 에러 응답 검증
        assert response.status_code == 400

    
    def test_login_success(self, api_client):
        # Given: 테스트용 사용자 생성
        User.objects.create_user(
            username="JIN HO",
            password="12341234",
            nickname="Mentos"
        )
        
        # When: 로그인 요청
        response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "12341234"
        })
        
        # Then: 응답 검증
        assert response.status_code == 200
        assert 'token' in response.data
    
    def test_login_wrong_password(self, api_client):
        # Given: 테스트용 사용자 생성
        User.objects.create_user(
            username="JIN HO",
            password="12341234",
            nickname="Mentos"
        )
        
        # When: 잘못된 비밀번호로 로그인 시도
        response = api_client.post('/accounts/login', {
            "username": "JIN HO",
            "password": "1234123"
        })
        
        # Then: 에러 응답 검증
        assert response.status_code == 401
        assert 'error' in response.data
