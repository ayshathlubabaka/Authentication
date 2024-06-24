from django.core.management.base import BaseCommand
from authentication.models import Role
from rest_framework.permissions import BasePermission


class Command(BaseCommand):
    help = 'Create initial roles'

    def handle(self, *args, **kwargs):
        Role.objects.get_or_create(name='companion')
        Role.objects.get_or_create(name='mentor')
        Role.objects.get_or_create(name='hr')
        self.stdout.write(self.style.SUCCESS('Roles created successfully'))


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='mentor').exists()

class IsCompanion(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='companion').exists()

class IsHr(BasePermission):
    def has_permission(self, request, view):
        return request.user.roles.filter(name='hr').exists()