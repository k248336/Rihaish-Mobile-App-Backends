from rest_framework import serializers
from .models import Property
from django.contrib.auth.models import User

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class PropertySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        return Property.objects.create(owner=user, **validated_data)
