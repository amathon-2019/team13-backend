from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.user.models import Token
from .serializers import (
    LoginSerializer, SignUpSerializer, DuplicateSerializer,
)
from .responses import (
    UserLoginSuccessResponse, UserLoginFailResponse,
    UserDuplicateResponse,
)


class LoginAPIView(GenericAPIView):
    """
    로그인 API
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.login()
        if user is None:
            return Response(
                UserLoginFailResponse.json(), 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token
        })


class SignUpAPIView(GenericAPIView):
    """
    회원가입 API
    """
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = generate_jwt_token(user)

        return Response({
            'token': token
        }, status=status.HTTP_201_CREATED)


class DuplicateAPIView(GenericAPIView):
    serializer_class = DuplicateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_duplicate = serializer.is_duplicate()

        return Response({
            'is_duplicate': is_duplicate
        })
