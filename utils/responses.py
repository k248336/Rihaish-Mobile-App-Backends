from rest_framework.response import Response
from rest_framework import status


def success_response(message: str, data=None, status_code=status.HTTP_200_OK):
    """Standard success response wrapper."""
    return Response(
        {
            "status": "success",
            "message": message,
            "data": data if data is not None else {},
        },
        status=status_code,
    )


def error_response(message: str, data=None, status_code=status.HTTP_400_BAD_REQUEST):
    """Standard error response wrapper."""
    return Response(
        {
            "status": "error",
            "message": message,
            "data": data if data is not None else {},
        },
        status=status_code,
    )
