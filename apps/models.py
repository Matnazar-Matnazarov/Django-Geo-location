from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension
# Create your models here.

class GeoLocation(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_checked = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='geolocations/', null=True, blank=True, validators=[validate_image_file_extension])
    description = models.TextField(null=True, blank=True)
    
 
    
    class Meta:
        ordering = ['-created_at']