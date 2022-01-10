from django.shortcuts import redirect, render, HttpResponse
from .forms import UsersSignupForm, UsersLoginForm, OTPEnterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.utils import timezone
from customauth.models import MyUser
from .utils import *

# Create your views here.

def test(request):
    send_mail(
        'This is my subject',
        'Secure access',
        'ssmailtest200@gmail.com',
        ['co18344@ccet.ac.in'],
        fail_silently=False,
    )
    return HttpResponse('<h1>Hi lets begin !!</h1>')

def signUp(request):
    if request.method == 'POST':
        form = UsersSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if checkIfEmailExists(email):
                Otp = fetchOtpExp(email)
                if timezone.now() > Otp.expiryTime:
                    updateOtp(Otp)
            else:
                Otp = saveOtp(email,otpGenerator())
            sendEmail(email, Otp.otp)

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.info(request,'Enter the otp sent to your email address')
            return render(request, '_parcelDelivery/otp-enter.html',{
                'mail':Otp.email,
            })
        else:
            # converted to list because original content was of type dict_keys, which was not subscriptable
            firstErrorKey = list(form.errors.keys())[0]
            message = list(form.errors.values())[0][0]
            messages.error(request, message)
            
    return render(request, '_parcelDelivery/sign-up.html')                                                

def logIn(request):
    if request.method == 'POST':
        form = UsersLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email = email, password = password)
            if user is not None:
                login(request,user)
                return redirect('/parcel/dashboard/')
            messages.error(request,'Invalid email address or password')
        else:    
            firstErrorKey = list(form.errors.keys())[0]
            message = form.errors.get(firstErrorKey)
            messages.error(request,message)
    return render(request, '_parcelDelivery/log-in.html')                                                

def dashboard(request):
    if request.user.is_anonymous:
        return redirect("/parcel/login/")
    return render(request, '_parcelDelivery/dashboard.html')

def logOut(request):
    messages.success(request,'Logged out successfully')
    logout(request)
    return redirect("/parcel/login/")

def addr(request):
    return render(request, '_parcelDelivery/address.html')

def verifyOtp(request):
    if request.method == 'POST':
        message = None
        form = OTPEnterForm(request.POST)
        emailBeforeValidation = request.POST.get('email','')
        if form.is_valid():
            email = form.cleaned_data['email']
            if checkIfEmailExists(email):
                Otp = fetchOtpExp(email)
                if timezone.now() > Otp.expiryTime:
                    messages.error('OTP expired')
                    return redirect('/parcel/create/')
                else:
                    if form.cleaned_data['otp'] == str(Otp.otp):
                        messages.success(request, 'OTP Verified!!. You can login now')
                        user = fetchUser(Otp.email)
                        user.is_active = True
                        user.save()

                        otpCleaner(email)

                        return redirect('/parcel/login/')
                    messages.error(request, 'Invaid OTP entered')
                    return redirect('/parcel/create/') 
            else:
                messages.error('Bad credentials')
                return redirect('/parcel/create/') 
                
        else:
            #firstErrorKey = list(form.errors.keys())[0]
            #message = form.errors.get(firstErrorKey)
            message = list(form.errors.values())[0][0]
            messages.error(request,message)

        return render(request, '_parcelDelivery/otp-enter.html',{
            'mail':emailBeforeValidation
        })
    return HttpResponse('<strong>Bad request</strong>')