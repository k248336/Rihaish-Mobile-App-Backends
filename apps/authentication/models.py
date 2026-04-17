from django.db import models

class OTPVerification(models.Model):
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} - {self.otp_code}"
