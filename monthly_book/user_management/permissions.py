from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):

    message = 'You are not authorized to view these details. Please contact your administrator.'

    def has_permission(self, request, view):
            return request.user.is_superuser