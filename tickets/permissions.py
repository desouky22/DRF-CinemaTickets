from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "U cant edit this post"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.author
