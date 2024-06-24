from django.core.mail import send_mail
import random
from django.conf import settings
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

def send_otp_via_email(email):
    print('inside signal')
    subject = "Your account verification email"
    otp = random.randint(100000, 999999)
    print(otp)
    message = f"Your otp is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = CustomUser.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()


