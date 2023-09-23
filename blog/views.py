from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserSerializer, RegisterUserSerializer, DescriptionSerializer, Select_Course_Serializer,\
                        Post_DescriptionSerializer, Post_Select_Course_Serializer, AddFriendSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import AbstractUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Description, Course, Friend, User
from django.http import Http404, HttpResponse
from rest_framework import generics
from .helper import details_send_mail, activationlink_send_mail, activationlink_send_mail1
from django.contrib.auth.hashers import make_password

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView

#using generics listapiview
# class UserListApi(generics.ListAPIView):
#     permission_classes = [AllowAny]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserDetailApi(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListApi(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
    serializer_class = UserSerializer
    def get(self, request, format=None):
        print(str(request.user),str(request.auth) ,'=============')
        items = User.objects.all()
        serializer = self.serializer_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class RegisterUser(APIView):
    serializer_class = RegisterUserSerializer
    def post(self, request, format=None):
        username = request.data['username']
        first_name = request.data['first_name']
        email = request.data['email']
        password = request.data['password']
        if password == request.data['confirm_password']:
            serializer = self.serializer_class(data={'username':username,\
                                                    'first_name':first_name, 'email':email, 'password':make_password(password)})
            if serializer.is_valid():
                serializer.validated_data
                serializer.save()
                serialized_data = serializer.data
                activationlink_send_mail(serialized_data)
                # details_send_mail(serialized_data)
                return Response({"data":serialized_data,"message": "Account activation link sent to mail"},status=status.HTTP_201_CREATED)
            return Response({"message": serializer.errors},status=status.HTTP_401_UNAUTHORIZED)  
        return Response({"message":"password and confirm password not matching"})
            
class PutDeleteUser(APIView):
    serialized_class = UserSerializer
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except:
            raise Http404
    def get(self, request,id, format=None):  
        item = self.get_object(id)
        serializer = self.serialized_class(item)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    def put(self, request, id, format=None):
        item = self.get_object(id)
        serializer = self.serialized_class(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format = None):
        item = self.get_object(id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class LoginUser(APIView):
    def post(self, request):
        username = request.data['username']
        password= request.data['password']
        print(password,'===============')
        try:
            user= User.objects.get(username=username)
            check_password =  user.check_password(password)
            print(check_password,'=========================')
            if check_password and user.is_verified:
                token = RefreshToken.for_user(user)
                data = {"user":user.first_name,"access_token":str(token.access_token),"refresh_token":str(token)}
                return Response(data)
            elif not user.is_verified:
                activationlink_send_mail1(user)
                data = {"user":user.username, "message":"your account is not verified.\
Link sent to your mail. Please verify your email for account activation"}
                return Response(data)
            else:
                data = {"user":user.username,'message':"wrong password"}
                return Response(data)
        except:
            data = {"user":"no user found"}
            return Response(data)

class ViewDesc(APIView):
    serializer_class = DescriptionSerializer
    def get(self, request, format=None):
        print(request.user)
        item = Description.objects.filter(written_by=request.user)
        serializer = self.serializer_class(item, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class PostDesc(APIView):
    serializer_class = Post_DescriptionSerializer
    def post(self, request, format=None):
        # request.data['user'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class PutDeleteDesc(APIView):
    serialized_class = DescriptionSerializer
    def get_object(self, id):
        try:
            return Description.objects.get(id=id)
        except:
            raise Http404
        
    def get(self, request, id, format=None):
        item = self.get_object(id)
        serializer = self.serialized_class(item)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        item = self.get_object(id)
        serializer = self.serialized_class(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        item = self.get_object(id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
class GetAllDescview(APIView):
    serialized_class = DescriptionSerializer
    def get(self, request):
        all_desc_obj = Description.objects.all()
        serializer = self.serialized_class(all_desc_obj, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class SelectCourse(APIView):
    serialized_class = Post_Select_Course_Serializer
    def post(self, request):
        serializer = self.serialized_class(data = request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response({'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllCourseUsers(APIView):
    serialized_class = Select_Course_Serializer
    def get(self, request):
        items = Course.objects.all()
        serializer = self.serialized_class(items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class Add_Friends(APIView):
    serialized_class = AddFriendSerializer
    def post(self, request):
        user = request.data['user']    
        friends = request.data['friend']   #type is list
        item = Friend.objects.filter(user=user)
        if item:
            friends.remove(user)
            # for i in friend:              
            # if i == user:
            #     continue
            item[0].friend.add(*friends)   #adding into manytomany field
            items = Friend.objects.get(user=user)        
            serializer = self.serialized_class(items)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        elif not item:
            serializer = self.serialized_class(data = request.data)
            for i in request.data['friend']:
                if i == request.data['user']:
                    request.data['friend'].remove(i)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
# class Add_Friends(APIView):
#     serialized_class = AddFriendSerializer
#     def post(self, request):
#         print(request.data, '*************((((((((((((((((((()))))))))))))))))))')
#         serializer = self.serialized_class(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             serialized_data = serializer.data
#             return Response(serialized_data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Get_Friends(APIView):
    serialized_class = AddFriendSerializer
    def get(self, request):
        items = Friend.objects.all()
        serializer = self.serialized_class(items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

class PutDeleteFriend(APIView):
    serializer_class = AddFriendSerializer
    def get_object(self, id):
        try:
            item = Friend.objects.get(id=id)
            return item
        except:
            raise Http404
    def get(self, request, id):
        serializer = self.serializer_class(self.get_object(id))
        serializer_data = serializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def put(self, request, id):
        item = self.get_object(id)
        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        item = self.get_object(id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class Activation:
#     def get(self, request, token, name):
#         item = User.objects.get(username=name)
#         item.is_verified = True
#         item.save()
#         return Response("account verified", status=status.HTTP_200_OK)

def Activation(request, token, name):
    item = User.objects.get(username=name)
    item.is_verified = True
    item.save()
    return HttpResponse('ACCOUNT VERIFIED')

