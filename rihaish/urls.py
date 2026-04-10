from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # This allows serving media files in production/Render if no other storage is used
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
