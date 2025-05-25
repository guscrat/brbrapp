from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class SomenteBarbeirosMixin(UserPassesTestMixin):
    """Permite acesso apenas a usuários com is_barbeiro=True"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_barbeiro

    def handle_no_permission(self):
        raise PermissionDenied("Você não tem permissão para acessar esta página.")

class SomenteClientesMixin(UserPassesTestMixin):
    """Permite acesso apenas a usuários com is_barbeiro=False"""
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_barbeiro

    def handle_no_permission(self):
        raise PermissionDenied("Você não tem permissão para acessar esta página.")
