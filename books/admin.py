from django.contrib import admin
from books.models import Book

class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('id', 'name' , 'category', 'user', 'created_date', 'updated_date') 
    search_fields = ['name']

admin.site.register(Book, BookAdmin)

