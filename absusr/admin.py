from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PaymentMethod, Category, Booking
# Register your models here.

fields = list(UserAdmin.fieldsets)
fields[0] = (None,{'fields':('email','password')})
fields[1] = ('Personal Details',{'fields':('full_name','phone_number','dateofbirth')})
UserAdmin.fieldsets = tuple(fields)

class UserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Address Details',{'fields':('Address_line1','Address_line2','city','state','zipcode')}),
        ('Verification Status',{'fields':('is_verified',)}),
    )
    list_display = ('email', 'full_name', 'phone_number','is_verified')

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('mail_id','card_number','card_holdername')
    def mail_id(self, obj):
        try:
            return obj.user.email
        except:
            return "Error"        
        
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('USER',{'fields':('user',)}),
        ('Çategories',{
            'fields':('category',)
        }),
        ('Personal Details',{
            'fields':('full_name','dateofbirth')
        }),
        ('Choose Notary Method',{
            'fields':('notary_method', 'documentupload_method')
        }),
        ('Address Details',{
            'fields':('state', 'city', 'zipcode', 'Address_line1', 'Address_line2')
        }),
        # ('Session Status',{
        #     'fields':('live_session_status',)
        # })
    ]
    list_display = ('full_name', 'category', 'user_mail')
    def user_mail(self, obj):
        try:
            return obj.user.email
        except:
            return "SOME ERROR"       

class BookingAdmin(admin.ModelAdmin):
    list_display = ('Customer_name','Notary_agent_name','status')    

admin.site.register(User, UserAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Booking,BookingAdmin)