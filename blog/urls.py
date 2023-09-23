from django.urls import path
from . import views
from . views import UserListApi, RegisterUser, LoginUser, ViewDesc, PutDeleteUser, PostDesc,\
      PutDeleteDesc, GetAllDescview, SelectCourse, GetAllCourseUsers, UserDetailApi,Add_Friends,\
      Get_Friends, PutDeleteFriend
urlpatterns = [
    path('api/ulist/', UserListApi.as_view()),
    path('api/ulist/<int:pk>/', UserDetailApi.as_view()),
    path('api/register/', RegisterUser.as_view()),
    path('api/putdeleteu/<int:id>/', PutDeleteUser.as_view()),
    path('api/login/', LoginUser.as_view()),
    path('api/dlist/', ViewDesc.as_view()),
    path('api/postd/', PostDesc.as_view()),
    path('api/putdeleted/<int:id>/', PutDeleteDesc.as_view()),
    path('api/get-all-desc/', GetAllDescview.as_view()),
    path('api/select-course/',  SelectCourse.as_view()),
    path('api/get-all-course&users/',  GetAllCourseUsers.as_view()),
    path('api/add-friends/',  Add_Friends.as_view()),
    path('api/get-all-friends/',  Get_Friends.as_view()),
    path('api/putdeletef/<int:id>/', PutDeleteFriend.as_view()),
    path('api/activationlink/<token>/<name>/', views.Activation),
]