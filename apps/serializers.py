from rest_framework import serializers
from django.contrib.auth.models import User
from .models import GeoLocation
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']



class GeoLocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GeoLocation 
        geo_field = 'location'
        fields = ['id', 'name', 'user', 'location', 'address', 'created_at', 'updated_at', 'picture', 'description']
        read_only_fields = ['id', 'created_at', 'updated_at']