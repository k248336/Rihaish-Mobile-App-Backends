from django.db import models
from django.contrib.auth.models import User
from apps.properties.models import Property


class Notification(models.Model):
    TYPE_CHOICES = [
        ('new_property', 'New Property'),
        ('property_liked', 'Property Liked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='triggered_notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.user.username} - {self.title}"
