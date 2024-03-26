from django.contrib import admin
from purchases.models import Purchase

class PurchaseAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ('id', 'description', 'user', 'price', 'book') 
    search_fields = ['book']

admin.site.register(Purchase, PurchaseAdmin)

