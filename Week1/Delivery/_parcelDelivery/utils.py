from django.core.mail import send_mail
from customauth.models import EmailOtp, getExpiryTime, MyUser
import random

def otpGenerator():
    start = 100000
    end = 999999  
    return random.randint(start, end)

def sendEmail(receiver, otp):
    send_mail(
        'One Time Password',
        'Your Secret OTP for email address verification is {}. The OTP is valid for 5 minutes'.format(otp),
        'ssmailtest200@gmail.com',
        [receiver],
        fail_silently=False,
    )

def checkIfEmailExists(email):
    return EmailOtp.objects.filter(email = email).exists()

def fetchOtpExp(email):
    return EmailOtp.objects.filter(email = email)[0]

def fetchUser(email):
    return MyUser.objects.filter(email=email)[0]

def saveOtp(email, otp):
    Otp = EmailOtp.objects.create(email = email, otp = otp)
    Otp.save()
    return Otp

def updateOtp(Otp):
    Otp.otp = otpGenerator()
    Otp.expiryTime = getExpiryTime()
    Otp.save()

def otpCleaner(email):
    fetchOtpExp(email).delete()