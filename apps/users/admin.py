from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'tanggal_dibuat')
    list_filter = ('role', 'is_active', 'is_staff', 'tanggal_dibuat')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'nomor_telepon')
    ordering = ('username',)
    
    # Fieldsets untuk halaman EDIT (setelah user dibuat)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {'fields': ('first_name', 'last_name', 'email', 'nomor_telepon', 'foto_profil')}),
        ('Role & Akses', {'fields': ('role', 'spesialisasi', 'nomor_str', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('tanggal_dibuat', 'tanggal_terakhir_login'), 'classes': ('collapse',)}),
    )
    
    # Fieldsets untuk halaman ADD (saat membuat user baru) - INI YANG KURANG!
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
                'nomor_str'
            ),
        }),
    )
    
    readonly_fields = ('tanggal_dibuat', 'tanggal_terakhir_login')