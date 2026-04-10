from django.urls import path
from .views import PropertyListCreateView, PropertyDetailView

urlpatterns = [
    # List and Create
    path('properties/all/', PropertyListCreateView.as_view(), name='property_list'),
    path('properties/create/', PropertyListCreateView.as_view(), name='property_create'),
    
    # Detail, Update, and Delete
    path('properties/detail/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('properties/update/<int:pk>/', PropertyDetailView.as_view(), name='property_update'),
    path('properties/delete/<int:pk>/', PropertyDetailView.as_view(), name='property_delete'),
]
