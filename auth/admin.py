from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PhoneOTP


class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'phone', 'admin',)
    list_filter = ('staff','active' ,'admin', )
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'introduction',)}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
        ),
    )


    search_fields = ('phone','name')
    ordering = ('phone','name')
    filter_horizontal = ()

class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'count')

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)

admin.site.unregister(Group)
