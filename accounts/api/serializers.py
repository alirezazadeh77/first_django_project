import random
from abc import ABC

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from accounts.models import User, VerifyCode
from first_project import settings
from product.validators import clean_phone_number_validator


class TokenLifetimeSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['expire'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class RefreshLifetimeSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['expire'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['Phone_number']

    def create(self, validated_data):
        phone_number = validated_data['Phone_number']

        try:
            user = User.objects.get(Phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(Phone_number=phone_number)

        if settings.DEVEL:
            verify_code = 22222
        else:
            verify_code = random.randint(10000, 99999)

        user.set_verify_code(verify_code)
        return user


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("new password and confirm password did not match")
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['request'].user

        if user.has_usable_password():
            raise serializers.ValidationError("this user has already set password before")
        user.set_password(validated_data['confirm_password'])
        user.save()
        return user


class SendVerifyCodeSerializer(serializers.Serializer):
    Phone_number = serializers.IntegerField(validators=[clean_phone_number_validator, ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            self.user = User.objects.get(Phone_number=attrs['Phone_number'])
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        return super().validate(attrs)

    def create(self, validated_data):
        if settings.DEVEL:
            verify_code = 22222
        else:
            verify_code = random.randint(10000, 99999)
        self.user.set_verify_code(verify_code)
        return self.user


class ForgotPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("new password and confirm password did not match")
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.has_usable_password():
            raise serializers.ValidationError("this user does not have password")
        user.set_unusable_password()
        user.set_password(validated_data['confirm_password'])
        user.save()
        return user
