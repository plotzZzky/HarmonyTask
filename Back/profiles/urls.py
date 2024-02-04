from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProfilesClassView.as_view()),
    path('your/', views.YourProfileClassView.as_view()),
    path('favorite/', views.FavoriteClassView.as_view()),
]
