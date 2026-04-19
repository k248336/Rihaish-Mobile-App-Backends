from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    LISTING_TYPE_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=50) # e.g. apartment, house, villa
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='sell')
    size = models.CharField(max_length=50) # e.g. 1500 sqft
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    washrooms = models.IntegerField(blank=True, null=True)
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)
    images = models.JSONField(default=list) # Store list of image URLs
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return f"{self.title} - {self.city}"
