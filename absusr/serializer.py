from .models import User, PaymentMethod, Category, Booking
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','full_name','phone_number','dateofbirth','state','city','zipcode',
                  'Address_line1','Address_line2','password']
        extra_kwargs = {"password":{"write_only":True}}     

class AddcardDetails(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id','user', 'card_number', 'card_holdername', 'expiry_date']        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','user','category','full_name','dateofbirth',\
                  'notary_method','documentupload_method','state','city',\
                  'zipcode','Address_line1','Address_line2']    
        
class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user','Customer_name','Notary_agent_name','Commission_Number',
                  'service_name','Notary_agent_charges','Delivery_charges','Service_charges',
                  'Total','status']        
        
class GetAllUserSerializer(serializers.ModelSerializer):
    card_details = serializers.SerializerMethodField()
    booking_details = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email','full_name','phone_number','dateofbirth','state','city','zipcode',
                  'Address_line1','Address_line2','card_details','booking_details']           
        
    def get_card_details(self, obj):
        email = getattr(obj, 'email')
        item = User.objects.get(email=email)
        cards = PaymentMethod.objects.filter(user_id=item.id).values()
        return cards    
    
    def get_booking_details(self, obj):
        email = getattr(obj, 'email')
        item = User.objects.get(email=email)
        bookings = Booking.objects.filter(user_id = item.id).values()
        return bookings
    
class EditDetailsSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','full_name','phone_number','dateofbirth','state','city','zipcode','Address_line1','Address_line2']    
        extra_kwargs = {"phone_number":{"required":True}}