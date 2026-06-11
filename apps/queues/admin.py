from django.contrib import admin
from .models import Antrian, LogNotifikasi


@admin.register(Antrian)
class AntrianAdmin(admin.ModelAdmin):
    list_display = ('nomor_antrian', 'pasien', 'jenis_layanan', 'status', 'prioritas', 'tanggal_daftar', 'dikelola_oleh')
    list_filter = ('status', 'jenis_layanan', 'prioritas', 'tanggal_daftar')
    search_fields = ('nomor_antrian', 'pasien__nama_lengkap', 'pasien__nrm')
    readonly_fields = ('nomor_antrian', 'tanggal_daftar')
    ordering = ('-tanggal_daftar',)
    
    fieldsets = (
        ('Informasi Antrian', {
            'fields': ('nomor_antrian', 'pasien', 'jenis_layanan', 'status', 'prioritas')
        }),
        ('Waktu', {
            'fields': ('tanggal_daftar', 'tanggal_panggil', 'tanggal_mulai', 'tanggal_selesai', 'estimasi_waktu_tunggu')
        }),
        ('Catatan & Pengelola', {
            'fields': ('catatan', 'dikelola_oleh')
        }),
    )

    # --- RBAC ---
    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.role in ['admin']
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.role in ['admin', 'dokter']
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated


@admin.register(LogNotifikasi)
class LogNotifikasiAdmin(admin.ModelAdmin):
    list_display = ('antrian', 'metode', 'tujuan', 'status', 'tanggal_kirim')
    list_filter = ('metode', 'status', 'tanggal_kirim')
    search_fields = ('antrian__nomor_antrian', 'tujuan', 'pesan')
    readonly_fields = ('tanggal_kirim',)
    ordering = ('-tanggal_kirim',)

    # --- RBAC ---
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.role in ['admin', 'dokter']