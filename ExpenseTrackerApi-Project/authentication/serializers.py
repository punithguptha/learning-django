from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

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
