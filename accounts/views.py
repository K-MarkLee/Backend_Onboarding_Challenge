from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            , status=status.HTTP_201_CREATED)
        print("Validation errors:", serializer.errors)  # 에러 출력 추가
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
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
            return Response({
                "token": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response({
            "error": "아이디 또는 비밀번호가 올바르지 않습니다."
        }, status=status.HTTP_401_UNAUTHORIZED)
