from rest_framework import routers

from . import views

profiles_router = routers.DefaultRouter()
profiles_router.register(r'all', views.ProfilesClassView, basename='all')
profiles_router.register(r'your', views.YourProfileClassView, basename='your')
profiles_router.register(r'favorites', views.FavoriteClassView, basename='favorite')
