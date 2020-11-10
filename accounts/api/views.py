from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase

from accounts.api.serializers import TokenLifetimeSerializer, RefreshLifetimeSerializer, RegisterSerializer, \
    SetPasswordSerializer, SendVerifyCodeSerializer, ForgotPasswordSerializer
from accounts.models import User
from first_project.throttles import PhoneNumberScopedReateTrottle


class TokenLifetimeView(TokenViewBase):
    serializer_class = TokenLifetimeSerializer


class RefreshLifetimeView(TokenViewBase):
    serializer_class = RefreshLifetimeSerializer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    throttle_classes = [PhoneNumberScopedReateTrottle, ]
    throttle_scope = "register"


class SetPasswordView(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("new password set successful", status=status.HTTP_201_CREATED)


class SendVerifyCodeView(APIView):
    throttle_classes = [PhoneNumberScopedReateTrottle, ]
    throttle_scope = "sendverifycode"

    def post(self, request, *args, **kwargs):
        serializer = SendVerifyCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("message is already send", status=status.HTTP_201_CREATED)


class ForgetPasswordView(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("new password set successful", status=status.HTTP_201_CREATED)
