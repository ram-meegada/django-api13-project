from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserRegistrationSerializer, AddcardDetails, CategorySerializer,\
                        BookingsSerializer, GetAllUserSerializer, EditDetailsSetupSerializer
from django.contrib.auth.hashers import make_password, check_password
from . models import User, Booking, PaymentMethod, Category
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from .helper import resetpwdlink, hostname, commission_num, activationlink_send_mail,\
                    activationlink_send_mail1, category_charges, gen_random_pwd

# Create your views here.
class UserRegisterAPI(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        password = request.data['password']
        request.data['password'] = make_password(password)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            activationlink_send_mail(serialized_data)
            return Response({"data":serialized_data, "message":"Account activation link sent to mail"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUsers(APIView):
    serializer_class = GetAllUserSerializer
    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        serialized_data = serializer.data
        return Response({"data":serialized_data}, status=status.HTTP_200_OK)

class EditUserDetails(APIView):
    serializer_class = EditDetailsSetupSerializer
    def get_object(self,id):
        try:
            return User.objects.get(id=id)
        except:
            raise Http404
    def get(self, request, id):
        user = self.get_object(id)
        serializer = self.serializer_class(user)
        serialized_data = serializer.data
        return Response({"data":serialized_data}, status=status.HTTP_200_OK)
    def put(self, request, id):
        user = self.get_object(id)
        serializer = self.serializer_class(user, data = request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            data = {"data":serialized_data, "message":"Details are updated"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)    
    
def Activation(request,token, identify):
    user= User.objects.get(email=identify)
    user.is_verified = True
    user.save()
    return HttpResponse(f"Your account is verified. Now you can sigin and set your profile")
    
class SignInAPI(APIView):
    def post(self, request):
        email = request.data['email']
        password= request.data['password']
        try:
            user= User.objects.get(email=email)
            check_pwd =  check_password(password,user.password)
            # item = Verification.objects.get(user_id=user.id)
            if check_pwd and user.is_verified:
                token = RefreshToken.for_user(user)
                data = {"user":user.email,"access_token":str(token.access_token),"refresh_token":str(token), "message":
"you are successfully logged in"}
                return Response(data)
            elif not check_pwd:
                data = {"message":"wrong password"}
                return Response(data)
            elif not user.is_verified:
                activationlink_send_mail1(user)
                data = {"user":user.email, "message":"your account is not verified.\
Link sent to your mail. Please verify your email for account activation"}
                return Response(data)
        except:
            data = {"user":"no user found"}
            return Response(data)
        
# class ProfileSetupAPI(APIView):
#     serializer_class = UserRegistrationSerializer
#     def post(self, request):
#         email = request.data['email']
#         try:
#             user = User.objects.get(email=email)
#             user.full_name = request.data["full_name"]
#             user.phone_number = request.data["phone_number"]
#             user.dateofbirth = request.data["dateofbirth"]
#             user.state = request.data["state"]
#             user.city = request.data["city"]
#             user.zipcode = request.data["zipcode"]
#             user.Address_line1 = request.data["Address_line1"]
#             user.Address_line2 = request.data["Address_line2"]
#             user.save()
#             serializer = self.serializer_class(user)
#             serializer_data = serializer.data
#             return Response(serializer_data, status=status.HTTP_200_OK)
#         except: 
#             return Response({"message":"ERROR!!!"}, status=status.HTTP_400_BAD_REQUEST) 

class ProfileSetupAPI(APIView):
    serializer_class = EditDetailsSetupSerializer
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except:
            raise Http404
    def get(self, request,id):
        user = self.get_object(id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, id):
        user = self.get_object(id)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            return Response({"data":serialized_data, "message":"Profile Details successfully updated"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordSign_link(APIView):
    def post(self, request):
        email = request.data['email']
        item = User.objects.filter(email=email)
        if item:
            resetpwdlink(item)
            data = {"message":"Forgot your password? Don't worry we will send you reset passsword link to your registered email"}
            return Response(data)
        elif not item:
            data = {"message":"Email not found. Please try again"}
            return Response(data)            

class ResetPassword(APIView):
    def post(self,request,token ,identify):
        item = User.objects.get(email=identify)
        New_password = request.data['password']
        # item.set_password(New_password)
        item.password = make_password(New_password)
        item.save()
        data = {"message":"Your password is successfully changed. Now you are being redirected to signin page"}
        return Response(data) 
    
class ChangePassword(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        email = request.data['email']
        current_password = request.data['password']
        New_password = request.data['New_password']    
        Confirm_Newpassword = request.data['Confirm_Newpassword']   
        item = User.objects.filter(email=email)
        if not item:
            data = {"message": "email not found. Please try again"}
            return Response(data)
        elif not check_password(current_password, item[0].password):
            data = {"message": "Old password is not correct"}
            return Response(data)
        elif New_password != Confirm_Newpassword:
            data = {"message":"newpasword and confirm new password are not matching"}
            return Response(data)
        elif New_password == Confirm_Newpassword:
            item[0].password = make_password(New_password)
            item[0].save()
            serializer = self.serializer_class(item[0])
            serialized_data = serializer.data
            return Response({"data": serialized_data, "message": "Password successfully updated"}, status=status.HTTP_202_ACCEPTED)    
        
class Add_card_details(APIView):
    serializer_class = AddcardDetails
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            return Response({"data":serialized_data, "message":"Card details successfully added"})
        return Response({"message": serializer.errors})        

class PaymentMethodsOfUser(APIView):
    serializer_class = AddcardDetails
    def get(self, request, id):
        methods = PaymentMethod.objects.filter(user_id=id)
        serializer = self.serializer_class(methods, many=True)
        serialized_data = serializer.data
        data = {"Payment Methods":serialized_data}
        return Response(data, status=status.HTTP_200_OK)    
    
class CategorySelection(APIView):
    serializer_class = CategorySerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            serialized_data = serializer.data
            cate = serialized_data["category"]
            host_name = hostname()
            catgry_chrg = category_charges()
            total=0
            Live_session_details={'host_name': host_name,
                    'commission_number':commission_num(),
                    'service_name':cate,
                    "PAYMENT_SUMMARY":{'notary_charges':catgry_chrg[cate],
                                        'service_charges':20,
                                        'delivery_charges':10,}}
            for i,j in (Live_session_details['PAYMENT_SUMMARY']).items():
                total += j 
            identifier = serialized_data['id']     
            Join_live_session = f"http://127.0.0.1:8000/api/joinlivesession/{identifier}/"
            Cancel_request = f"http://127.0.0.1:8000/api/cancelrequest/{identifier}/"    
            crt=Booking.objects.create(user_id=request.data['user'],Customer_name=request.data['full_name'],Notary_agent_name=host_name,\
                                       Commission_Number=commission_num(),service_name=request.data['category'],Notary_agent_charges=catgry_chrg[cate],\
                                       Total=total)
            crt.save()
            return Response({"data":serialized_data,"Live_session_details":Live_session_details, "Total":total,\
                             "Join_live_session":Join_live_session, "cancel request":Cancel_request}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinLiveSession(APIView):
    def get(self,request, identifier):
        item = Category.objects.get(id=identifier)
        # a = Booking.objects.filter(user_id=item.user.id).values()[::-1]
        a = Booking.objects.filter(user_id=item.user.id)[::-1]
        item_booking = a[0]
        item_booking.status="2"
        item_booking.save()
        # item.live_session_status = "2"
        # item.save()
        identity = item_booking.id
        message = "Your live session has been successfully completed. The notary agent will send documents to your address shortly"
        Payment_Details = {"Invoice Details":{"Customer Name":item_booking.Customer_name, "Notary Agent Name":item_booking.Notary_agent_name,\
                                              "Commission Number":item_booking.Commission_Number, "Service Name":item_booking.service_name},\
                           "Payment Summary":{"Notary Agent Charges":item_booking.Notary_agent_charges, "Delivery Charges":\
                                              item_booking.Delivery_charges, "Service_charges":item_booking.Service_charges,\
                                              "Total":item_booking.Total},
                           "Choose_Payment_Method":{'Credit card/Debit card/Net Banking':
                                                    f"http://127.0.0.1:8000/payment/{identity}/"}}
        return Response({"message":message,"Payment_Details":Payment_Details})

class Cancel_request(APIView):
    def get(self, request, identifier):
        item = Category.objects.get(id=identifier)
        # a = Booking.objects.filter(user_id=item.user.id).values()[::-1]
        a = Booking.objects.filter(user_id=item.user.id)[::-1]
        item_booking = a[0]
        item_booking.status="3"
        item_booking.save()
        message = "Session Cancelled. Now you will be redirected to home"
        return Response({"message":message})    

# class PaymentAPI(APIView):
#     def get(self, request, identity):
#         item = Booking.objects.get(id=identity)
#         item.status = "1"
#         item.save()
#         message = f"Your payment of {item.Total} has been successfully paid. You can check the details in My Bookings"
#         return Response({"message":message})
    
class home(APIView):
    def get(self, request, identity):
        host = request.get_host()
        item = Booking.objects.get(id=identity)
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            # 'amount': '10.00',
            'amount': f"{item.Total}",
            'item_name': f"{item.service_name}",
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
            # 'return_url': 'http://{}{}'.format(host,reverse('paypal_return')),
            'return_url': f"http://127.0.0.1:8000/paypal_return/{identity}/",
            'cancel_return': 'http://{}{}'.format(host,reverse('paypal_cancel'))
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form':form}
        return render(request, 'home.html', context)

def paypal_return(request, identity):
    messages.success(request, 'payment succesfull')
    item = Booking.objects.get(id=identity)
    item.status = "1"
    item.save() 
    return HttpResponseRedirect(reverse('home', args=(identity,)))

def paypal_cancel(request):
    messages.error(request, 'your order cancelled')
    return HttpResponseRedirect(reverse('home'))    