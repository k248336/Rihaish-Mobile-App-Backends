from django.urls import path
from .views import PropertyListCreateView, PropertyDetailView

urlpatterns = [
    path('properties', PropertyListCreateView.as_view(), name='property_list_create'),
    path('properties/<int:pk>', PropertyDetailView.as_view(), name='property_detail'),
]
