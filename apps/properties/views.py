from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Property
from .serializers import PropertySerializer
from utils.responses import success_response, error_response
from utils.permissions import IsOwnerOrReadOnly
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import uuid
import os
import json

class PropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Property.objects.all().order_by('-created_at')
        
        # Filters
        prop_type = self.request.query_params.get('type', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        city = self.request.query_params.get('city', None)
        search = self.request.query_params.get('search', None)

        if prop_type:
            queryset = queryset.filter(property_type__icontains=prop_type)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) | 
                Q(city__icontains=search)
            )
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response("Properties retrieved successfully", data=serializer.data)

    def create(self, request, *args, **kwargs):
        # Handle image files if provided
        uploaded_files = request.FILES.getlist('uploaded_images')
        image_urls = []
        
        # Also check if 'images' were provided as a JSON string (for compatibility)
        existing_images = request.data.get('images', '[]')
        if isinstance(existing_images, str):
            try:
                image_urls = json.loads(existing_images)
            except json.JSONDecodeError:
                image_urls = []
        elif isinstance(existing_images, list):
            image_urls = existing_images

        # Process new file uploads
        for file_obj in uploaded_files:
            if file_obj.content_type.startswith('image/'):
                ext = os.path.splitext(file_obj.name)[1]
                filename = f"properties/{request.user.id}_{uuid.uuid4().hex}{ext}"
                path = default_storage.save(filename, ContentFile(file_obj.read()))
                url = request.build_absolute_uri(settings.MEDIA_URL + path)
                image_urls.append(url)

        # Prepare data for serializer
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data.copy()
        data['images'] = image_urls
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Property created successfully", data=serializer.data, status_code=201)
        return error_response("Invalid data", data=serializer.errors)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Property details retrieved successfully", data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Handle image files if provided
        uploaded_files = request.FILES.getlist('uploaded_images')
        
        # Start with existing images if it's a partial update (PATCH)
        # or if the user explicitly provided an 'images' list in the data
        image_urls = []
        existing_images = request.data.get('images', None)
        
        if existing_images is not None:
            if isinstance(existing_images, str):
                try:
                    image_urls = json.loads(existing_images)
                except json.JSONDecodeError:
                    image_urls = []
            elif isinstance(existing_images, list):
                image_urls = existing_images
        elif partial:
            # If it's a PATCH and no 'images' field provided, keep current images
            image_urls = instance.images

        # Process new file uploads and append to the list
        for file_obj in uploaded_files:
            if file_obj.content_type.startswith('image/'):
                ext = os.path.splitext(file_obj.name)[1]
                filename = f"properties/{request.user.id}_{uuid.uuid4().hex}{ext}"
                path = default_storage.save(filename, ContentFile(file_obj.read()))
                url = request.build_absolute_uri(settings.MEDIA_URL + path)
                image_urls.append(url)

        # Prepare data for serializer
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data.copy()
        if uploaded_files or existing_images is not None:
            data['images'] = image_urls
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response("Property updated successfully", data=serializer.data)
        return error_response("Invalid data", data=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response("Property deleted successfully")
