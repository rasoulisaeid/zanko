from django.contrib import admin
from bookmarks.models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('category', 'point', 'user','created_date', 'updated_date')   

admin.site.register(Bookmark, BookmarkAdmin)
