from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "admin"
    
class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "customer"