from rest_framework import serializers
from .models import Notification
from apps.properties.models import Property
from apps.properties.serializers import OwnerSerializer


class SimplePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'city', 'price']


class NotificationSerializer(serializers.ModelSerializer):
    related_property = SimplePropertySerializer(read_only=True)
    related_user = OwnerSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'message', 'related_property', 'related_user', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']
