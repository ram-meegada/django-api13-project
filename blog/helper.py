from django.core.mail import send_mail
from django.conf import settings
import random
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from .models import Contact_US_model

#code for text details email automation
def details_send_mail(serialized_data):
    email_id = 'stefenwarner13@gmail.com'
    email_pass = 'iyutbwcpmhehhmuc'
    msg = EmailMessage()
    msg['Subject'] = 'Contact Us Detail'
    msg['From'] = email_id
    msg['To'] = serialized_data['email']
    username,firstName,email, = serialized_data['username'], serialized_data['first_name'],serialized_data['email']
    msg.set_content( f" username:{username} \n first Name:{firstName} \n email : {email} \n")   
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(email_id, email_pass)
        mail.send_message(msg)

def activationlink_send_mail(serialized_data):
    email_id = 'stefenwarner13@gmail.com'
    email_pass = 'iyutbwcpmhehhmuc'
    msg = EmailMessage()
    msg['Subject'] = 'Activation link'
    msg['From'] = email_id
    msg['To'] = serialized_data['email']
    token = generate_token()
    name = serialized_data['username']
    msg.set_content(f"http://127.0.0.1:8000/api/activationlink/{token}/{name}/")   
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(email_id, email_pass)
        mail.send_message(msg)   

def activationlink_send_mail1(user):
    email_id = 'stefenwarner13@gmail.com'
    email_pass = 'iyutbwcpmhehhmuc'
    msg = EmailMessage()
    msg['Subject'] = 'Activation link'
    msg['From'] = email_id
    msg['To'] = user.email
    token = generate_token()
    name = user.username
    msg.set_content(f"http://127.0.0.1:8000/api/activationlink/{token}/{name}/")   
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(email_id, email_pass)
        mail.send_message(msg)        


def generate_token():
    otp = ''
    num = "1234567890"
    for i in range(4):
        otp += random.choice(num)
    return otp
    