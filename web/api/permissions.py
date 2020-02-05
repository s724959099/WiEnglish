from rest_framework.permissions import BasePermission
from functools import partial
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.authentication import get_authorization_header, exceptions
from .models import AdminTokens, Manager


class DefaultIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return True
        user = request.user
        token = request.auth
        if isinstance(user, Manager) and token and not token.expired():
            return True
        else:
            return False


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        token = request.auth
        if isinstance(user, Manager) and token and not token.expired():
            return True
        else:
            return False
