from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Schema and Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1 routes
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.properties.urls')),
    path('api/v1/', include('apps.favorites.urls')),
    path('api/v1/', include('apps.location.urls')),
    path('api/v1/', include('apps.chat.urls')),
    path('api/v1/', include('apps.profile.urls')),
    path('api/v1/', include('apps.upload.urls')),
    path('api/v1/', include('apps.settings_app.urls')),

    # Media files serving - works in both DEBUG and Production
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
