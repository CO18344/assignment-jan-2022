from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields
from django.forms.widgets import PasswordInput
from customauth.models import MyUser

class UsersSignupForm(forms.ModelForm):
    # this form field is not part of the model
    cpwd=forms.CharField(widget=forms.PasswordInput())

    # these fields are part of the database as well as form
    class Meta:
        model = MyUser
        fields = ('email', 'name', 'phone', 'country', 'state', 'city', 'zipCode', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmedPassword = cleaned_data.get('cpwd')

        if password and confirmedPassword and password != confirmedPassword:
            print('password and confirmPassword don"t match')
            raise ValidationError([
                ValidationError('password and confirmPassword don"t match', code='error1'),
                ])
    def is_already_present(self):
        return MyUser.objects.filter(email=self.cleaned_data['email']).exists()

class UsersLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput())

class OTPEnterForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(label='otp')