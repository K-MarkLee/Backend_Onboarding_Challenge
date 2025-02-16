from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer


class SignUpView(APIView):
    @swagger_auto_schema(
        operation_description="회원가입 API",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="로그인 API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 아이디'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호'),
            },
        ),
        responses={
            200: openapi.Response(
                description="로그인 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='액세스 토큰'),
                    }
                )
            ),
            400: "아이디와 비밀번호를 모두 입력해주세요.",
            401: "아이디 또는 비밀번호가 올바르지 않습니다."
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "error": "아이디와 비밀번호를 모두 입력해주세요."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({
                "token": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

            response['X-Refresh-Token'] = str(refresh)
            return response

        return Response({
            "error": "아이디 또는 비밀번호가 올바르지 않습니다."
        }, status=status.HTTP_401_UNAUTHORIZED)


class RefreshView(APIView):
    @swagger_auto_schema(
        operation_description="토큰 갱신 API",
        manual_parameters=[
            openapi.Parameter(
                'X-Refresh-Token',
                openapi.IN_HEADER,
                description="리프레시 토큰",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="토큰 갱신 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='새로운 액세스 토큰'),
                    }
                )
            ),
            401: "유효하지 않은 리프레시 토큰"
        }
    )
    def post(self, request):
        try:
            refresh_token = request.headers.get('X-Refresh-Token')

            if not refresh_token:
                return Response({
                    "error": "refresh token을 찾을 수 없습니다."
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            return Response({
                "token": new_access_token
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
