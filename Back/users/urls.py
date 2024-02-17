from rest_framework import routers

from . import views

user_router = routers.DefaultRouter()
user_router.register(r'login', views.LoginView, basename='login')
user_router.register(r'register', views.RegisterView, basename='register')
user_router.register(r'recovery', views.RecoveryPassword, basename='recovery')
user_router.register(r'question', views.ReceiverYourQuestion, basename='question')
