from django.contrib import admin
from .models import AssessmentMedis


@admin.register(AssessmentMedis)
class AssessmentMedisAdmin(admin.ModelAdmin):
    list_display = ('pasien', 'dokter', 'tanggal_assessment', 'status', 'diagnosis')
    list_filter = ('status', 'tanggal_assessment', 'dokter')
    search_fields = ('pasien__nama_lengkap', 'pasien__nrm', 'diagnosis', 'keluhan_utama')
    readonly_fields = ('tanggal_assessment', 'tanggal_dibuat', 'tanggal_diupdate')
    ordering = ('-tanggal_assessment',)
    
    fieldsets = (
        ('Informasi Pasien & Dokter', {
            'fields': ('pasien', 'dokter', 'antrian', 'tanggal_assessment', 'status')
        }),
        ('Data Assessment', {
            'fields': ('keluhan_utama', 'riwayat_penyakit', 'hasil_pemeriksaan', 'diagnosis', 'catatan_medis')
        }),
        ('Rencana Terapi', {
            'fields': ('rencana_terapi', 'frekuensi_terapi', 'durasi_terapi')
        }),
        ('Metadata', {
            'fields': ('tanggal_dibuat', 'tanggal_diupdate'),
            'classes': ('collapse',)
        }),
    )

    # --- RBAC: Pembatasan Akses ---
    def has_add_permission(self, request):
        # Hanya Admin dan Dokter yang bisa tambah assessment
        return request.user.is_superuser or request.user.role in ['admin', 'dokter']
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.role in ['admin', 'dokter']
    
    def has_delete_permission(self, request, obj=None):
        # Hanya Admin yang bisa hapus
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated
    
    # Filter assessment yang ditampilkan berdasarkan role
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Jika Dokter, hanya tampilkan assessment yang dia buat
        if request.user.role == 'dokter' and not request.user.is_superuser:
            return qs.filter(dokter=request.user)
        return qs