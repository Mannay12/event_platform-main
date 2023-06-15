from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from users.models import UserProfile


class IsEventPlannerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Allow GET, HEAD, OPTIONS requests to all users
            return True

        if not request.user.is_authenticated:
            # Deny all other requests if user is not authenticated
            return False

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'event_planner':
                # Allow edit requests only for event planners
                return True
        except UserProfile.DoesNotExist:
             raise PermissionDenied('User profile does\'t exist')

        # Deny all other requests
        return False