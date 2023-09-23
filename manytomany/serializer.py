from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'your_descriptions']  

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['username','first_name', 'email', 'password', 'confirm_password']       


class AddCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['user','course']         