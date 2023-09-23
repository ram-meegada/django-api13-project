import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def activationlink_send_mail(serialized_data):
    email_id = 'stefenwarner13@gmail.com'
    email_pass = 'iyutbwcpmhehhmuc'
    msg = EmailMessage()
    msg['Subject'] = 'Activation link'
    msg['From'] = email_id
    msg['To'] = serialized_data['email']
    token = generate_token()                                     
    identify = serialized_data['email']
    msg.set_content(f"http://127.0.0.1:8000/api/activationlink/{token}/{identify}/")
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
    identify = user.email
    msg.set_content(f"http://127.0.0.1:8000/api/activationlink/{token}/{identify}/")   
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(email_id, email_pass)
        mail.send_message(msg)        


def resetpwdlink(item):
    email_id = 'stefenwarner13@gmail.com'
    email_pass = 'iyutbwcpmhehhmuc'
    msg = EmailMessage()    
    msg['Subject'] = 'Reset password link'
    msg['From'] = email_id
    msg['To'] = item[0].email
    identify = item[0].email
    token = generate_token()  
    msg.set_content(f"http://127.0.0.1:8000/api/RestPassword/{token}/{identify}/")   
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(email_id, email_pass)
        mail.send_message(msg)  

def gen_random_pwd():
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"
    pwd = ""
    for i in range(10):
        pwd += random.choice(char)
    return pwd    

def generate_token():
    otp = ''
    num = "1234567890"
    for i in range(4):
        otp += random.choice(num)
    return otp        

def commission_num():
    otp = ''
    char = "1234567890"
    for i in range(14):
        otp += random.choice(char)
    return otp    

def hostname():
    hosts =("Dany wellington","Sarkar","Bishnoi","Pandya","Russel")
    host = random.choice(hosts)
    return host

def category_charges():
    catgry_chrg = {"1":100, "2":150, "3":200, "4":125, "5":320, "6":250, "7":300, "8":175}
    return catgry_chrg