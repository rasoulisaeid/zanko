from django.contrib import admin
from points.models import Point, TagPoint
class PointAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('id', 'chapter', 'type', 'image', 'voice', 'created_date', 'updated_date') 
    search_fields = ['chapter']    

admin.site.register(Point, PointAdmin)


class TagPointAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ('point', 'tag')    

admin.site.register(TagPoint, TagPointAdmin)