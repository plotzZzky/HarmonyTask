from django.urls import path

from . import views


urlpatterns = [
    path('all/', views.get_all_professionals),
    path('', views.get_professional_profile),
    path('your/', views.get_your_profile),
    path('update/', views.update_your_profile),
    path('favorites/', views.get_your_favorites),
    path('favorites/add/', views.add_professional_favorites),
]
