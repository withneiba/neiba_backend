from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import User, Product
from django.contrib.auth import authenticate


#User Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.IntegerField(required=True)
    tokens = serializers.CharField(max_length=100, min_length=6, read_only=True)
    password = serializers.CharField(write_only=True, max_length=100, min_length=4, required=True)

    class Meta:
        model= User
        fields = ['email','name','phone_number','password','tokens']


    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Phone number already exists')

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data['name']
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        user = User.objects.create_user(email,name,phone_number,password)
        user.save()
        return user



#login User
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    tokens = serializers.CharField(max_length=100, min_length=6, read_only=True)
    password = serializers.CharField(write_only=True, max_length=100, min_length=4, required=True)

    class Meta:
        model= User
        fields = ['email','tokens','password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not authenticate(email=email, password=password):
            raise serializers.ValidationError("Email or Password is invalid")

        user = User.objects.filter(email=email).first()

        return {
            'tokens':user.tokens()
        }





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'