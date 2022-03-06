from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

class RegisterSerializer(serializers.ModelSerializer):
    # write_only field doesnt send this info to the enduser in the response
    password=serializers.CharField(max_length=68,min_length=6,write_only=True)

    class Meta:
        model=User
        fields=['email','username','password']

    def validate(self,attrs):
        email=attrs.get('email','')
        username=attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError("The username should only contain alphanumeric characters")
        return attrs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=500)

    class Meta:
        model=User
        fields=['token']


class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,min_length=6,write_only=True)
    username=serializers.CharField(max_length=255,read_only=True)
    email=serializers.EmailField(max_length=255)
    tokens=serializers.CharField(max_length=500,read_only=True)

    class Meta:
        model=User
        fields=['username','email','password','tokens']

    def validate(self,attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')
        user=auth.authenticate(email=email,password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified..Complete the verification and try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled. Please contact your administrator")

        return {
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens
        }

class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)
    # Note: In class Meta of a serializer we need to mention model param only if the serializer inherits model serializer
    class Meta:
        fields=['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6,max_length=68,write_only=True)
    token=serializers.CharField(min_length=1,write_only=True)
    uidb64=serializers.CharField(min_length=1,write_only=True)

    class Meta:
        fields=['password','token','uidb64']

    def validate(self,attrs):
        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            id= force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid',401)
            # For updating or setting passwords this is the best method since it encrypts the passwords and stores in the db
            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
                raise AuthenticationFailed('The reset link is invalid',401)
        return super().validate(attrs)
