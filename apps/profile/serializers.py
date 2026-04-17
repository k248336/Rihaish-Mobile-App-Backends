from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('avatar_url', 'phone', 'bio', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('id', 'username', 'email')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile = instance.profile
        profile.avatar_url = profile_data.get('avatar_url', profile.avatar_url)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.save()

        return instance
