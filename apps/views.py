from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from rest_framework import viewsets, permissions, filters
from .models import GeoLocation
from .serializers import GeoLocationSerializer, UserSerializer
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json
from django.contrib.gis.geos import Point
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import googlemaps


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email'] 

class GeoLocationViewSet(viewsets.ModelViewSet):
    queryset = GeoLocation.objects.all()
    serializer_class = GeoLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'address']


class IndexView(View):
    
    def get(self, request):
        context = {
            'google_api_key': settings.GOOGLE_API_KEY,
            'map_id': settings.GOOGLE_MAP_ID
        }
        print(context)
        return render(request, 'index.html', context)

    def post(self, request):
        try:
            data = json.loads(request.body)
            latitude = float(data.get('latitude'))
            longitude = float(data.get('longitude'))
            
            # Google Maps Geocoding API orqali manzilni olish
            gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
            reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
            print(latitude, longitude)
            address = ''
            building_name = ''
            place_name = ''
            
            if reverse_geocode_result:
                result = reverse_geocode_result[0]
                address = result['formatted_address']
                
                # Joy/bino nomini izlash
                if 'name' in result:
                    place_name = result['name']
                
                # Bino nomini address_components dan izlash
                for component in result['address_components']:
                    if any(type in component['types'] for type in [
                        'point_of_interest',
                        'establishment',
                        'premise',
                        'subpremise'
                    ]):
                        building_name = component['long_name']
                        break
                
                # Plus code ni olib tashlash (8763+6VR kabi)
                if 'plus_code' in result:
                    plus_code = result['plus_code']['compound_code']
                    address = address.replace(plus_code.split(' ', 1)[0], '').strip()
                
                # Agar place_name yoki building_name topilgan bo'lsa, manzilga qo'shish
                final_name = place_name or building_name
                if final_name and final_name not in address:
                    address = f"{final_name}, {address}"
            
            location = Point(longitude, latitude, srid=4326)
            
            # GeoLocation obyektini yangilash yoki yaratish
            geolocation, created = GeoLocation.objects.update_or_create(
                user=request.user if request.user.is_authenticated else None,
                defaults={
                    'location': location,
                    'address': address,
                    'name': place_name or building_name or None
                }
            )
            
            return JsonResponse({
                'status': 'success',
                'address': address,
                'building_name': place_name or building_name
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
@require_http_methods(["GET"])
def google_maps_proxy(request):
    """Proxy view for Google Maps API requests"""
    try:
        base_url = 'https://maps.googleapis.com/maps/api/js'
        params = request.GET.dict()
        params['key'] = settings.GOOGLE_API_KEY
        params['map_id'] = settings.GOOGLE_MAP_ID
        
        response = requests.get(base_url, params=params)
        
        proxy_response = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
        
        # CORS headerlarini qo'shish
        proxy_response["Access-Control-Allow-Origin"] = "*"
        proxy_response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        proxy_response["Access-Control-Allow-Headers"] = "Content-Type"
        
        return proxy_response
        
    except Exception as e:
        return HttpResponse(
            content=f"Error: {str(e)}",
            status=500,
            content_type='text/plain'
        )

@require_http_methods(["GET"])
def get_maps_config(request):
    """Return Maps configuration"""
    return JsonResponse({
        'mapId': settings.GOOGLE_MAP_ID
    })
