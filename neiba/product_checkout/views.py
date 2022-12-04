from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer, ProductSerializer
from .models import User, Product, ProductBought
import ast
from .utils import Error
from rest_framework import viewsets
from rest_framework.request import Request




class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):

        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            email = serializer.data['email']
            token = serializer.data['tokens']
            user = User.objects.filter(email=email)

            k = ast.literal_eval(token)

            return Response({
                'msg': 'Registration was successful',
                'token': {"refresh": k['refresh'], "access": k['access']}
            }, status=status.HTTP_200_OK)
        else:
            error = Error().error(serializer.errors)
            return Response({"errors": error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.data['email']
            token = serializer.data['tokens']
            user = User.objects.filter(email=email)

            k = ast.literal_eval(token)

            return Response({
                'msg': 'Registration was successful',
                'token': {"refresh": k['refresh'], "access": k['access']}
            }, status=status.HTTP_200_OK)
        else:
            error = Error().error(serializer.errors)
            return Response({"errors": error['errors'][0]}, status=status.HTTP_400_BAD_REQUEST)




class ProductView(viewsets.ViewSet):
    def list(self,request:Request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(instance=queryset,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        queryset = Product.objects.get(pk=kwargs.get('pk'))
        serializer = ProductSerializer(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)



