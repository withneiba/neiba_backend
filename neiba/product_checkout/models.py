from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from cloudinary.models import CloudinaryField
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken



class CustomAccountManager(BaseUserManager):
    def create_superuser(self,email,name,password,phone_number, **other_field):
        other_field.setdefault('is_staff',True)
        other_field.setdefault('is_superuser',True)
        other_field.setdefault('is_active',True)

        if other_field.get('is_staff') is not True:
            return ValueError('superuser must have is_staff=True')
        if other_field.get('is_superuser') is not True:
            return ValueError('superuser must have is_superuser=True')

        return self.create_user(email,name,password,phone_number, **other_field)

    def create_user(self,email,name,phone_number,password, **other_field):
        if not email:
            return ValueError('Email must exist')

        if not name:
            return ValueError('You need to add your name')

        if not phone_number:
            return ValueError('Please add phone number')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,phone_number=phone_number, **other_field)
        user.set_password(password)
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.IntegerField(unique=True)
    address = models.CharField(max_length=300)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number','name']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh_token),
            'access':str(refresh_token.access_token)
        }



class Product(models.Model):
    product_name = models.CharField(max_length=300)
    expiry = models.DateTimeField()
    number_of_participant = models.IntegerField()
    max_participant = models.IntegerField()
    price = models.IntegerField()
    product_image = CloudinaryField('product_image', blank=True)


class ProductBought(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


