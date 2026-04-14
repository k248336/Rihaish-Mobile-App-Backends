from django.urls import path
from .views import NearbyPropertiesView

urlpatterns = [
    path('properties/nearby/', NearbyPropertiesView.as_view(), name='nearby_properties'),
]
