from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Description, Course, Friend, User
maxlen = 0
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255)
    # confirm_password = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['username','first_name', 'email', 'password'] 
        # read_only_fields = ['confirm_password']
        extra_kwargs = {'confirm_password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name']        

class DescriptionSerializer(serializers.ModelSerializer):
    lengthy_record = serializers.SerializerMethodField()
    written_by = UserSerializer()
    class Meta:
        model = Description
        fields = ['id', 'description', 'created_at', 'lengthy_record', 'written_by']

    def get_lengthy_record(self, description_object):
        global maxlen
        description = getattr(description_object, 'description')
        if description and len(description) > maxlen:
            maxlen = len(description)
            return maxlen
        return maxlen
    
class Post_DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'description', 'created_at','written_by']    

class Select_Course_Serializer(serializers.ModelSerializer):
    # most_selected_course = serializers.SerializerMethodField()
    course_opters = UserSerializer(many=True)
    class Meta:
        model = Course
        fields = ['course', 'course_opters']



class Post_Select_Course_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course', 'course_opters']
    # def get_most_selected_course(self, course_object):
    #     pass    , read_only=True

class AddFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend']