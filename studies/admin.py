from django.contrib import admin
from studies.models import Study

class StudyAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('id','point', 'user', 'level', 'order', 'function', 'created_date', 'updated_date') 
    search_fields = ['point']    

admin.site.register(Study, StudyAdmin)
