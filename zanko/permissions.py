from rest_framework import permissions


# Every user should only access to their data.
class JustOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        return object.user == request.user