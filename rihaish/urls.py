from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 routes
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.properties.urls')),
    path('api/v1/', include('apps.favorites.urls')),
    path('api/v1/', include('apps.location.urls')),
    path('api/v1/', include('apps.chat.urls')),
    path('api/v1/', include('apps.profile.urls')),
    path('api/v1/', include('apps.upload.urls')),
    path('api/v1/', include('apps.settings_app.urls')),
]
