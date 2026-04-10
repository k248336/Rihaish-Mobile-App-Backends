from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Favorite
from apps.properties.models import Property
from .serializers import FavoriteSerializer
from utils.responses import success_response, error_response

class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Favorites retrieved successfully", data=serializer.data)

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, property_id):
        try:
            property_obj = Property.objects.get(id=property_id)
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                property=property_obj
            )
            if created:
                return success_response("Property added to favorites")
            return success_response("Property is already in favorites")
        except Property.DoesNotExist:
            return error_response("Property not found", status_code=404)

    def delete(self, request, property_id):
        try:
            property_obj = Property.objects.get(id=property_id)
            deleted, _ = Favorite.objects.filter(user=request.user, property=property_obj).delete()
            if deleted:
                return success_response("Property removed from favorites")
            return error_response("Property not found in favorites", status_code=404)
        except Property.DoesNotExist:
            return error_response("Property not found", status_code=404)
