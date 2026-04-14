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
            favorite_qs = Favorite.objects.filter(
                user=request.user,
                property=property_obj
            )
            
            if favorite_qs.exists():
                favorite_qs.delete()
                return success_response("Property removed from favorites")
            else:
                Favorite.objects.create(
                    user=request.user,
                    property=property_obj
                )
                return success_response("Property added to favorites")
        except Property.DoesNotExist:
            return error_response("Property not found", status_code=404)
