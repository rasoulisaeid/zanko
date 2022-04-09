from django.contrib import admin
from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('id', 'name','user' , 'created_date', 'updated_date') 

admin.site.register(Tag, TagAdmin)
