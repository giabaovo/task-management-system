import random

from django.core.mail import send_mail
from django.conf import settings

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
