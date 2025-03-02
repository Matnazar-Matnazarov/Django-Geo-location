from django.urls import path
from .views import GeoLocationViewSet, UserViewSet, IndexView, google_maps_proxy, get_maps_config
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'geolocations', GeoLocationViewSet, basename='geolocations')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('maps-api/', google_maps_proxy, name='maps_proxy'),
    path('maps-api/config/', get_maps_config, name='maps_config'),
] + router.urls
