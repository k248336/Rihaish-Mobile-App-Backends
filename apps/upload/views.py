from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from utils.responses import success_response, error_response
from utils.supabase_client import upload_image
import uuid
import os

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES.get('image')
        
        if not file_obj:
            return error_response("No image file provided")
            
        # Check file type
        if not file_obj.content_type.startswith('image/'):
            return error_response("File must be an image")

        try:
            # Generate unique filename
            ext = os.path.splitext(file_obj.name)[1]
            filename = f"images/{request.user.id}_{uuid.uuid4().hex}{ext}"
            
            # Upload to Supabase
            public_url = upload_image(file_obj, filename)
            
            return success_response("Image uploaded successfully", data={"url": public_url}, status_code=201)
        except Exception as e:
            return error_response(f"Upload failed: {str(e)}", status_code=500)
