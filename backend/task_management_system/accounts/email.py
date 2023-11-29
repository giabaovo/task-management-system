import random

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status

from accounts.models import Account

def send_verify_email(email):
    email_subject = "Please active your account"
    otp = f"{random.randint(1000,9999):04d}"
    email_content = "Your verify code is {}, this code will be expire in 5 minutes".format(otp)
    email_from = settings.EMAIL_HOST_USER
    send_mail(email_subject, email_content, email_from, [email])
    user = Account.objects.get(email=email)
    user.otp = otp
    user.save()

def send_verify_forgot_password_email(email):
    email_subject = "Please confirm your email"
    otp = f"{random.randint(1000,9999):04d}"
    email_content = "Your verify code is {}, this code will be expire in 5 minutes".format(otp)
    email_from = settings.EMAIL_HOST_USER
    send_mail(email_subject, email_content, email_from, [email])
    user = Account.objects.get(email=email)
    user.otp = otp
    user.save()

def check_expire_email(otp, user_otp, user_otp_created_at):
    expiration_time = timezone.timedelta(minutes=5)
    if timezone.now() - user_otp_created_at < expiration_time:
        if user_otp != otp:
            return Response({"status": "error", "message": "Invalid OTP code"}, status=status.HTTP_400_BAD_REQUEST)
    else:    
        return Response({"status": "error", "message": "Your OTP code has been expire"}, status=status.HTTP_400_BAD_REQUEST)