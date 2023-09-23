from . import views
from django.urls import path
from .views import UserRegisterAPI, SignInAPI, ProfileSetupAPI, ForgotPasswordSign_link,ResetPassword,\
                   ChangePassword, Add_card_details, CategorySelection, JoinLiveSession, Cancel_request,\
                   PaymentMethodsOfUser, GetAllUsers, EditUserDetails, home

urlpatterns = [
    path('api/register/', UserRegisterAPI.as_view()),
    path('api/getallusers/', GetAllUsers.as_view()),
    path('api/activationlink/<token>/<identify>/', views.Activation),
    path('api/edituserdetails/<int:id>/', EditUserDetails.as_view()),
    path('api/signinapi/', SignInAPI.as_view()),
    path('api/profilesetupapi/<int:id>/', ProfileSetupAPI.as_view()),
    path('api/ForgotPasswordSign/', ForgotPasswordSign_link.as_view()),
    path('api/paymentmethodsofuser/<int:id>/', PaymentMethodsOfUser.as_view()),
    path('api/RestPassword/<token>/<identify>/', ResetPassword.as_view()),
    path('api/ChangePassword/', ChangePassword.as_view()),
    path('api/addcarddetails/', Add_card_details.as_view()),
    path('api/categoryselection/', CategorySelection.as_view()),
    path('api/joinlivesession/<identifier>/', JoinLiveSession.as_view()),
    path('api/cancelrequest/<identifier>/', Cancel_request.as_view()),
    # path('api/paymentmethod/<identity>/', PaymentAPI.as_view()),
    path('payment/<identity>/', home.as_view(), name="home"),
    path('paypal_return/<identity>/', views.paypal_return, name="paypal_return"),
    path('paypal_cancel', views.paypal_cancel, name="paypal_cancel"),
]