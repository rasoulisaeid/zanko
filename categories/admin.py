from django.contrib import admin
from categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('id', 'name' , 'user', 'created_date', 'updated_date') 
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)
