from django.urls import path,include
from .views import RegisterView, LoginView, ProductView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('',ProductView, basename='products')

urlpatterns = [
    path('auth/register',RegisterView.as_view(), name='register'),
    path('auth/login',LoginView.as_view(), name='login'),
    path("products/",include(router.urls)),
]