from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'tanggal_dibuat')
    list_filter = ('role', 'is_active', 'is_staff', 'tanggal_dibuat')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'nomor_telepon')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {'fields': ('first_name', 'last_name', 'email', 'nomor_telepon', 'foto_profil')}),
        ('Role & Akses', {'fields': ('role', 'spesialisasi', 'nomor_str', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('tanggal_dibuat', 'tanggal_terakhir_login'), 'classes': ('collapse',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email', 
                'password1', 
                'password2', 
                'role', 
                'first_name', 
                'last_name', 
                'nomor_telepon', 
                'spesialisasi', 
                'nomor_str',
            ),
        }),
    )
    
    readonly_fields = ('tanggal_dibuat', 'tanggal_terakhir_login')
    
    # **RBAC: Batasi siapa yang bisa manage User**
    def has_add_permission(self, request):
        # Hanya Admin dan Staff yang bisa tambah user
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_change_permission(self, request, obj=None):
        # Hanya Admin dan Staff yang bisa edit user
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_delete_permission(self, request, obj=None):
        # Hanya Superuser yang bisa hapus user
        return request.user.is_superuser