# Backend_Onboarding_Challenge

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Requirements](#requirements)
4. [Features](#features)
5. [Trouble-Shooting](#trouble-shooting)
6. [Refactor](#refactor)
<br>

<a name="introduction"></a>
## Introduction
### Backend Onboarding Challenge
바로 인턴 백엔드 온보딩 챌리지 구현

**[Service Link](13.125.8.202)**

## Duration
2025-02-13 ~ 2025-02-16

<br>
<a name="setup"></a>

## Setup
To set up and run the project, please follow the steps below:

1. Clone the repository
    ```
    git clone https://github.com/K-MarkLee/Backend_Onboarding_Challenge
    ```

2. Navigate to the repository
    ```
    cd Backend_Onboarding_Challenge
    ```

3. Install dependencies
    ```
    pip install -r requirements.txt
    ```

4. Create .env file
    ```
    SECRET_KEY
    DEBUG
    DB_NAME 
    DB_USER 
    DB_PASSWORD         
    DB_HOST 
    DB_PORT 
    ip4 
    ```

5. Run the project with docker
    ```
    docker-compose up -d
    ```

6. Access the project
    ```
    http://localhost:8000
    ```

<br>
<a name="requirements"></a>

## Requirements
1. Pytest를 이용한 테스트 코드 작성법 이해
2. Django를 이용한 인증과 권한 이래
3. JWT와 구체적인 알고리즘의 이해
4. PR 날려보기
5. 리뷰 바탕으로 개선
6. EC2 연결과 서버 실행


<br>
<a name="features"></a>

## Features
1. 회원가입/ 로그인/ refreshToken 구현하기
    [tests.py](https://github.com/K-MarkLee/Backend_Onboarding_Challenge/blob/main/accounts/views.py)
    ![signup](https://github.com/user-attachments/assets/1616314e-f193-44d4-8c47-06d96f163acf)
    ![login](https://github.com/user-attachments/assets/cc1c3f12-7040-426d-b3ea-2d357ab59a9e)
3. urls 구현하기
    [urls.py](https://github.com/K-MarkLee/Backend_Onboarding_Challenge/blob/main/accounts/urls.py)
4. 유닛 테스트 진행하기
    ![tests](https://github.com/user-attachments/assets/eb3e1852-caf6-4cec-8bef-3991f59bee9a)
5. Swagger UI 연결하기
    ![swagger](https://github.com/user-attachments/assets/10df4184-f607-4a18-b892-27c9d4c49946)
7. AWS EC2 연결하기
    [Swagger](http://13.125.8.202)
8. AI 를 통한 코드 리뷰 받아보기 (Refactor 파트로)
10. 피드백 받아 코드 개선하기 (Refactor 파트로)
11. AWS EC2 재배포 하기
12. PR 관리하기
    [PR](https://github.com/K-MarkLee/Backend_Onboarding_Challenge/pulls?q=is%3Apr+is%3Aclosed)
    ![pr](https://github.com/user-attachments/assets/1779a275-6d09-4d41-95d6-8303c23d9c2c)


<br>


<a name="trouble-shooting"></a>

## Trouble-Shooting
작업중 생긴 트러블 슈팅

1. Signup의 테스트 케이스가 통과되지 못함
    - 원인 : Signup의 response가 테스트 케이스와 일치 하지 않음. 리스트로 딕셔너리를 감싸는 형태로, 딕셔너리 안에 유저의 데이터가 응답되야하는데, views에 `Response("user" : serializer.data)`를 사용하고 있음. user로 한번 더 감싸게 되어서 다른 결과값을 응답함.

    - 해결방법 : Response에서 user로 감싸지 않고 바로 seailizer.data로 데이터를 응답하게함. 이때, serializer.data의 데이터 형태는 model에서 설정한 형태로 나오기 때문에 model의 설정을 확인해야함.

    - 결과 : response의 형태는 올바르나 아직 signup의 response가 통과되지 않음.



2. Signup의 테스트 케이스가 통과되지 못함
    - 원인 : 다양한 테스트를 통하여, signup에 테스트 비밀번호가 password validation을 통과하지 못하여 생긴 문제라는 것을 확인. serialzer에 유저의 비밀번호 최소 검증을 위한 django 기본 auth password validator를 사용하였는데, 이를 통과하지 못하고 생긴 문제

    - 해결방법 : settings의 auth_password_validator의 numericpassword(숫자로만 이루어진 비밀번호 제한) 와 commonpassword(너무 쉬운 비밀번호 제한)를 삭제.

    - 결과 : password validartor가 잘 작동하고 Signup의 테스트 케이스도 통과함.

3. JWT 리프레시 토큰 전당 방식 불일치
    - 원인 : 요청사항을 따르면, login시 access token만을 응답해야함. 이때, refresh 토큰을 따로 설정 해두지 않아서 access token을 재생성 할 수 없음

    - 해결방법 : refresh 토큰을 header에 넣기 위해서 커스텀 RefreshView를 작성. refresh를 호출하면 헤더에서 refresh token을 가져와서 access token을 재생성하게함.

    - 결과 : access token의 재생성 테스트 케이스 실패

4. TokenRefreshView의 충돌
    - 원인 : refresh token을 헤더에 적용시키기 위해서 커스텀 View를 생성했는데, urls.py에서 아직 DRF 의 기존 RokenRefreshView를 사용하고 있음. 

    - 해결방법 : TokenRefreshView를 RefreshView(커스텀) 으로 변경을 하고, 테스트를 실행

    - 결과 : 테스트 케이스 통과

5. Django Admin 로그인 페이지 리다이렉트 문제
    - 문제 : EC2에서 도메인 접속시 swagger ui대신 django admin 로그인 페이지로 이동.
    - 원인 : Django REST Framework의 기본 인증 설정이 인증을 요구, Swagger Ui 접근시 인증을 요구. 

    - 해결방법 : settings의 rest_framework의 permission을 allowany로 설정. Swagger 에 session auth를 비활성화함. urls의 admin페이지를 삭제.

    - 결과 : 해결 완료

6. Nginx에서 Ip의 노출 문제
    - 문제 : Nginx에서 ip의 노출이 되는 문제.

    - 해결방법 : nginx.conf대신 nginx/default.conf.template를 사용하고, ip를 .env에서 가져옴.

    - 결과 : 해결은 완료 했다만, 생각해보니 도메인 자체를 생성하지 않았기에 노출 해도 큰 문제는 없었을 것. (ec2 ip 접속을 내 아이피로 제한해둠)


<br>

<a name = "refactor"></a>

## Refactor
AI의 코드 리뷰를 통한 리팩토링 실시.


1. model에서 CustomUser에 필요 없는 함수 (Role Select)가 있다.
    - Role Select는 create user에서 유저의 Role을 설정하기 위한 함수였지만, 이를 통하지 않고 바로 role을 설정하게 변경했음. 이때 Role Select를 남겨둔 것.

    - 삭제완료

2. serializers에서 password의 필드가 중복으로 정의되었다.
    - password가 **kwargs와 validate_password에 중복으로 정의되고 있었음. validate_password 를 커스텀해서 사용하고 있기 때문에 **kwargs에서는 더이상 password릐 설정이 필요하지 않음.

    - 삭제완료

3. views 에서 에러 메시지를 중복되게 처리를 하고 있다.
    - views에서 Return response 로 http응답과 에러 메시지를 띄웠는데 중복으로 print(serializer.errors)를 사용하고 있음. 중복된 에러 메시지 반환을 제거후 통합함.

    - 완료



