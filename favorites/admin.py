from django.contrib import admin
from favorites.models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('name', 'created_date', 'updated_date') 
   
admin.site.register(Favorite, FavoriteAdmin)
