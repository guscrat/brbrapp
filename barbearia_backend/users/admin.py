from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_barbeiro', 'is_staff', 'date_joined')
    list_filter = ('is_barbeiro', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    # Adiciona o campo is_barbeiro ao formulário de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil Barbearia', {'fields': ('is_barbeiro',)}),
    )
    
    # Adiciona o campo is_barbeiro ao formulário de criação
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Perfil Barbearia', {'fields': ('is_barbeiro',)}),
    )