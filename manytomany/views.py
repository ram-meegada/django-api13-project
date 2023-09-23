from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserSerializer, RegisterUserSerializer, AddCoursesSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Course
from django.http import Http404
# Create your views here.
class UserListApi(APIView):
    serializer_class = UserSerializer
    def get(self, request, format=None):
        items = User.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
        #return Response(serialized_data, status=status.HTTP_200_OK)
    
class RegisterUser(APIView):
    serializer_class = RegisterUserSerializer
    def post(self, request, format=None):
        username = request.data['username']
        first_name = request.data['first_name']
        email = request.data['email']
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        if password == confirm_password:
            user = User.objects.create(username=username, first_name=first_name, email=email)
            user.set_password(password)
            user.save()
            # items = User.objects.filter(username=user.username).values()
            # print(items)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
class AddCourses(APIView):
    serializer_class = AddCoursesSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            
            return Response(serialized_data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)