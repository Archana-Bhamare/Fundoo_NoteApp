from rest_framework import serializers
from .models import UserDetails


class RegisterationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'


class LoginFormFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['username', 'password']

class ForgotPasswordFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['email']

class ResetPasswordFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['password','confirm_password']
