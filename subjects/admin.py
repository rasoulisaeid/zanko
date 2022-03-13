from django.contrib import admin
from subjects.models import Subject

class SubjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('name', 'chapter' ,'created_date', 'updated_date') 
    search_fields = ['chapter']

admin.site.register(Subject, SubjectAdmin)
