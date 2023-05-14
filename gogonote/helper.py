from django.core.mail import send_mail
from cryptography.fernet import Fernet
from django.conf import settings

from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from gogonote.models import userentry

def confirmation_mailing(user_name,email, token):
    html_msg = render_to_string('email_template_Confirmation.html', {'user_name':user_name,'email': email, 'token': token})
    subject = 'Confirmation email link'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    msg = strip_tags(html_msg)
    email = EmailMultiAlternatives(
        subject,
        msg,
        email_from,
        recipient_list
    )
    email.attach_alternative(html_msg, "text/html")
    email.send()

    print("success confirmation_mailing")
    return True

def send_password_encrypted(user_name,password, email):
    with open("gogonote/keyfile.key", 'rb') as file:
        key =  file.read()

    f = Fernet(key)
    enc_pass = str(f.encrypt(password.encode()))
    print(enc_pass)
    enc_pass = "dark" + enc_pass[2:-1] + email
    print(enc_pass)

    data_to_send = str(f.encrypt(enc_pass.encode()))
    data_to_send = data_to_send[2:-1]
    print(data_to_send)

    html_msg = render_to_string('email_template_secret_key.html', {'user_name':user_name,'email': email, 'token': data_to_send})
    subject = 'Recovery/Secret Key '

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    msg = strip_tags(html_msg)
    email = EmailMultiAlternatives(
        subject,
        msg,
        email_from,
        recipient_list
    )
    email.attach_alternative(html_msg, "text/html")
    email.send()
    return True

def forget_password_mail(user_name,email, token):

    html_msg = render_to_string('email_template_Reset_Password.html', {'user_name':user_name,'email': email, 'token': token})
    msg = strip_tags(html_msg)

    subject = 'Your forget password link'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email = EmailMultiAlternatives(
        subject,
        msg,
        email_from,
        recipient_list
    )
    email.attach_alternative(html_msg, "text/html")
    email.send()

    print("success forget_password_mail mail")
    # message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
    # send_mail(subject, msg, email_from, recipient_list, fail_silently=False,)
    
    return True



