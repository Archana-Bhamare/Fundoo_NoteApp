from rest_framework import serializers
from django.contrib.auth.models import User

from Note_App.models import Registration


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(validated_data)

class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


