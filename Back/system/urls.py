from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings

from users.urls import user_router
from profiles.urls import profiles_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(user_router.urls)),
    path('profiles/', include(profiles_router.urls)),
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
]
