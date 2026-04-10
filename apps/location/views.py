from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.properties.models import Property
from apps.properties.serializers import PropertySerializer
from utils.responses import success_response, error_response
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

class NearbyPropertiesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 10) # default 10km

        if not lat or not lng:
            return error_response("Latitude and longitude are required")

        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
        except ValueError:
            return error_response("Invalid coordinates")

        # Get all properties with coordinates
        properties_with_location = Property.objects.exclude(
            location_lat__isnull=True
        ).exclude(location_lng__isnull=True)

        nearby_properties = []
        for prop in properties_with_location:
            dist = haversine(lat, lng, prop.location_lat, prop.location_lng)
            if dist <= radius:
                # We can inject distance into the object if needed, but for now just filter
                prop.distance = dist
                nearby_properties.append(prop)

        # Sort by distance
        nearby_properties.sort(key=lambda x: getattr(x, 'distance', float('inf')))

        serializer = PropertySerializer(nearby_properties, many=True)
        return success_response("Nearby properties retrieved successfully", data=serializer.data)
