from django.contrib import admin
from .models import Laporan


@admin.register(Laporan)
class LaporanAdmin(admin.ModelAdmin):
    list_display = ('judul_laporan', 'tipe_laporan', 'dibuat_oleh', 'status', 'periode_mulai', 'periode_selesai', 'tanggal_dibuat')
    list_filter = ('tipe_laporan', 'status', 'tanggal_dibuat', 'dibuat_oleh')
    search_fields = ('judul_laporan', 'ringkasan_isi')
    readonly_fields = ('tanggal_dibuat', 'tanggal_diupdate', 'tanggal_dikirim')
    ordering = ('-tanggal_dibuat',)
    
    fieldsets = (
        ('Informasi Laporan', {
            'fields': ('dibuat_oleh', 'tipe_laporan', 'judul_laporan', 'status')
        }),
        ('Periode & Isi', {
            'fields': ('periode_mulai', 'periode_selesai', 'ringkasan_isi', 'data_lengkap')
        }),
        ('File & Timestamps', {
            'fields': ('file_pdf', 'tanggal_dibuat', 'tanggal_diupdate', 'tanggal_dikirim')
        }),
    )

    # --- RBAC: Hanya Admin yang bisa akses Laporan ---
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.role in ['admin', 'dokter']