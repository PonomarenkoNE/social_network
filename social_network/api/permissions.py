from rest_framework.permissions import BasePermission


class IsOwnerOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.creator == request.user


class IsOwnerOrSuperuserOrPostOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.creator == request.user
