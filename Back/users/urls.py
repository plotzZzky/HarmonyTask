from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('recovery/', views.RecoveryPassword.as_view()),
    path('question/', views.ReceiverYourQuestion.as_view())
]
