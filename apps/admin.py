from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import GeoLocation
from django.conf import settings

@admin.register(GeoLocation)
class GeoLocationAdmin(GISModelAdmin):
    list_display = ['name', 'user', 'location', 'address', 'created_at', 'updated_at', 'picture']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['name', 'address', 'description']
    ordering = ['-created_at']
    list_per_page = 25
    list_max_show_all = 200
    
    # Fields that can be edited from the list view
    list_editable = ['address']
    
    # Fields that link to the change view
    list_display_links = ['name']
    
    # Related fields to select in one query
    list_select_related = ['user']
    
    # Fields to display in the edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'user', 'description')
        }),
        ('Location Details', {
            'fields': ('location', 'address')
        }),
        ('Media', {
            'fields': ('picture',)
        })
    )
    
    # Map settings
    map_width = 800
    map_height = 500
    default_zoom = 13
    default_lon = 69.2797  # Tashkent longitude
    default_lat = 41.3111  # Tashkent latitude
    
    # Google Maps settings
    map_template = 'gis/admin/google.html'
    extra_js = [
        f'https://maps.googleapis.com/maps/api/js?key={settings.GOOGLE_API_KEY}&callback=Function.prototype'
    ]

    # Customize widget settings
    gis_widget_kwargs = {
        'attrs': {
            'default_lon': default_lon,
            'default_lat': default_lat,
            'default_zoom': default_zoom,
        }
    }

