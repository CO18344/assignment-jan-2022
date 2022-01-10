from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone, country, state, city , zipCode ,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not name:
            raise ValueError('Name can"t be empty')

        if not phone:
            raise ValueError('Phone Number can"t be empty')

        if not country:
            raise ValueError('Country can"t be empty')

        if not state:
            raise ValueError('State can"t be empty')

        if not city:
            raise ValueError('City can"t be empty')
        
        if not zipCode:
            raise ValueError('ZipCode can"t be empty')
        
        if not password:
            raise ValueError('Password can"t be empty')

        user = self.model(
            email = self.normalize_email(email),
            # fname = fname,
            # lname=lname,
        )

        # country , state, city , zip code
        user.set_password(password)
        user.name = name
        user.phone = phone
        user.country = country
        user.state = state
        user.city = city
        user.zipCode = zipCode

        user.save(using=self._db)
        return user

    def create_superuser(self,email,name,phone,country,state,city,zipCode,password=None):
        user = self.create_user(
            email,
            name = name,
            phone=phone,
            country = country,
            state = state,
            city = city,
            zipCode = zipCode,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=500)
    phone = PhoneNumberField()
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    zipCode = models.CharField(max_length=500)
 
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Field that will be asked when creating super user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone','country', 'state', 'city' , 'zipCode']

    objects = MyUserManager()
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


def getExpiryTime():
    return timezone.now() + timezone.timedelta(minutes=5)

class EmailOtp(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    expiryTime = models.DateTimeField(default=getExpiryTime)

    def __str__(self):
        return self.email

