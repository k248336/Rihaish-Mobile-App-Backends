from django.apps import AppConfig
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentication'

    def ready(self):
        logger.info("=== Authentication App Starting ===")
        logger.info(f"OTP_BACKEND: {settings.OTP_BACKEND}")
        logger.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        logger.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        logger.info(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        logger.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        logger.info(f"EMAIL_HOST_PASSWORD is set: {bool(settings.EMAIL_HOST_PASSWORD)}")
