import os
from supabase import create_client, Client
from django.conf import settings


def get_supabase_client() -> Client:
    """Initialize and return Supabase client."""
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    return create_client(url, key)


def upload_image(file_obj, file_path: str) -> str:
    """
    Uploads an image file to Supabase storage.
    Returns the public URL of the uploaded file.
    """
    supabase = get_supabase_client()
    bucket_name = settings.SUPABASE_BUCKET

    # Upload file
    response = supabase.storage.from_(bucket_name).upload(
        file=file_obj.read(),
        path=file_path,
        file_options={"content-type": file_obj.content_type}
    )

    # Get public URL
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
    return public_url


def delete_image(file_path: str):
    """Deletes an image from Supabase storage."""
    supabase = get_supabase_client()
    bucket_name = settings.SUPABASE_BUCKET
    supabase.storage.from_(bucket_name).remove([file_path])
