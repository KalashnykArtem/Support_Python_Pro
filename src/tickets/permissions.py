from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from tickets.models import Ticket
from users.constants import Role
from users.models import User


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


class RoleIsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.MANAGER


class RoleIsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.USER


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj: Ticket):
        return obj.user == request.user


class IsNewManager(BasePermission):
    def has_permission(self, request, view):
        new_manager_id = request.data["manager_id"]

        try:
            user = User.objects.get(id=new_manager_id)
        except User.DoesNotExist:
            raise PermissionDenied("You can only enter an existing manager ID")
        ticket_id = request.parser_context["kwargs"]["pk"]

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise PermissionDenied("You can only enter an existing ticket ID")

        if user.role != Role.MANAGER:
            raise PermissionDenied("You can only enter a manager ID")

        if ticket.manager_id == new_manager_id:
            raise PermissionDenied("You can only enter a new manager ID")

        return True
