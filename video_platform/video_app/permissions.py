from rest_framework.permissions import BasePermission


class PublishedOrOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Ограничение по опубликованным видеозаписям"""
        if obj.is_published:
            return True

        return obj.owner == request.user
