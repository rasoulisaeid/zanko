from django.contrib import admin
from chapters.models import Chapter

class ChapterAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('name', 'book' ,'created_date', 'updated_date') 
    search_fields = ['book']

admin.site.register(Chapter, ChapterAdmin)