from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUser(permissions.BasePermission):
    """
    Permission qui autorise uniquement les admins (is_staff=True).
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    

class IsOwnerOrAdmin(BasePermission):
    """Autorise uniquement le propriétaire de l'objet ou un admin"""
    def has_object_permission(self, request, view, obj):
        return request.user and (obj == request.user or request.user.is_staff)
    

class IsOwner(BasePermission):
    """Autorise uniquement le propriétaire de l'objet ou un admin"""
    def has_object_permission(self, request, view, obj):
        return request.user and (obj == request.user)


class IsTeacher(BasePermission):
    """Autorise uniquement si l'utilisateur est teacher"""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'teacher'
    


class IsStudent(BasePermission):
    """Autorise uniquement si l'utilisateur est student"""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'student'
    

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
  

class IsAuthenticatedAndActive(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active