from django.contrib import admin
from points.models import Point
class PointAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('subject','explains', 'rtl', 'image', 'voice', 'created_date', 'updated_date') 
    search_fields = ['subject']    

admin.site.register(Point, PointAdmin)
