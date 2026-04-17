from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import uuid
import os
from .serializers import UserSerializer
from utils.responses import success_response, error_response

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Profile retrieved successfully", data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Handle avatar file if uploaded
        avatar_url = None
        uploaded_avatar = request.FILES.get('avatar')
        if uploaded_avatar:
            if uploaded_avatar.content_type.startswith('image/'):
                ext = os.path.splitext(uploaded_avatar.name)[1]
                filename = f"avatars/{request.user.id}_{uuid.uuid4().hex}{ext}"
                path = default_storage.save(filename, ContentFile(uploaded_avatar.read()))
                path_url = path.replace('\\', '/')
                avatar_url = request.build_absolute_uri(settings.MEDIA_URL + path_url)
        
        # Prepare data for serializer - handle nested profile updates
        data = request.data.copy()
        
        # Get existing profile data from request if any
        profile_data = {}
        
        # Extract profile fields from root (since form-data can't send nested JSON)
        if 'phone' in data:
            profile_data['phone'] = data.get('phone')
        if 'bio' in data:
            profile_data['bio'] = data.get('bio')
        
        # Always use our new uploaded avatar_url, ignore any existing one in data
        if avatar_url:
            profile_data['avatar_url'] = avatar_url
        
        # If we have any profile data to update, structure it as nested
        if profile_data:
            data['profile'] = profile_data
        
        # Convert QueryDict to dict and ensure our profile data is preserved
        if hasattr(data, 'dict'):
            final_data = data.dict()
            if 'profile' in data:
                final_data['profile'] = profile_data
        else:
            final_data = data
        
        # Now update the user and profile
        serializer = self.get_serializer(instance, data=final_data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response("Profile updated successfully", data=serializer.data)
        return error_response("Invalid data", data=serializer.errors)
