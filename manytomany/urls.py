from django.urls import path
from .views import UserListApi, RegisterUser, AddCourses
urlpatterns = [
    path('api/ulist/', UserListApi.as_view()),
    path('api/register/', RegisterUser.as_view()),
     path('api/addcourses/', AddCourses.as_view()),
]