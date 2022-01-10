from django.urls import path
from . import views

urlpatterns = [
    path('test/',views.test, name='test url'),
    path('create/',views.signUp, name='new account'),
    path('login/',views.logIn, name='log in'),
    path('verify_otp/',views.verifyOtp, name='verify otp'),
    path('dashboard/',views.dashboard, name='Dash Board'),
    path('dashboard/logout/',views.logOut, name='log out'),
    path('address/',views.addr, name='new1 account'),
] 