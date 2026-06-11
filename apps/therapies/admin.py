from django.contrib import admin
from .models import Terapi, MonitoringTerapi


@admin.register(Terapi)
class TerapiAdmin(admin.ModelAdmin):
    list_display = ('pasien', 'nama_terapi', 'terapis', 'status', 'tanggal_mulai', 'frekuensi')
    list_filter = ('status', 'nama_terapi', 'tanggal_mulai', 'terapis')
    search_fields = ('pasien__nama_lengkap', 'pasien__nrm', 'deskripsi_terapi')
    readonly_fields = ('tanggal_dibuat', 'tanggal_diupdate')
    ordering = ('-tanggal_mulai',)
    
    fieldsets = (
        ('Informasi Terapi', {
            'fields': ('pasien', 'assessment', 'terapis', 'nama_terapi', 'status')
        }),
        ('Deskripsi & Jadwal', {
            'fields': ('deskripsi_terapi', 'tanggal_mulai', 'tanggal_selesai', 'frekuensi', 'durasi_per_sesi')
        }),
        ('Catatan', {
            'fields': ('catatan',)
        }),
        ('Metadata', {
            'fields': ('tanggal_dibuat', 'tanggal_diupdate'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MonitoringTerapi)
class MonitoringTerapiAdmin(admin.ModelAdmin):
    list_display = ('pasien', 'terapi', 'terapis', 'tanggal_sesi', 'kehadiran', 'durasi_aktual')
    list_filter = ('kehadiran', 'tanggal_sesi', 'terapis')
    search_fields = ('pasien__nama_lengkap', 'terapi__nama_terapi', 'catatan_perkembangan')
    readonly_fields = ('tanggal_sesi', 'tanggal_dibuat')
    ordering = ('-tanggal_sesi',)
    
    fieldsets = (
        ('Informasi Sesi', {
            'fields': ('terapi', 'pasien', 'terapis', 'tanggal_sesi', 'durasi_aktual', 'kehadiran')
        }),
        ('Catatan Perkembangan', {
            'fields': ('kondisi_pasien', 'catatan_perkembangan', 'pencapaian_target', 'rekomendasi_sesi_berikutnya')
        }),
        ('Metadata', {
            'fields': ('tanggal_dibuat',),
            'classes': ('collapse',)
        }),
    )
    
@admin.register(Terapi)
class TerapiAdmin(admin.ModelAdmin):
    # ... fieldsets dan list_display yang sudah ada ...
    
    # **RBAC: Pembatasan Akses**
    def has_add_permission(self, request):
        # Admin dan Dokter yang bisa jadwal terapi
        return request.user.is_superuser or request.user.role in ['admin', 'dokter']
    
    def has_change_permission(self, request, obj=None):
        # Terapis yang menangani bisa edit, Admin dan Dokter juga bisa
        if request.user.is_superuser or request.user.role in ['admin', 'dokter']:
            return True
        if request.user.role == 'terapis' and obj:
            return obj.terapis == request.user
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Hanya Admin yang bisa hapus
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated
    
    # **Filter terapi berdasarkan terapis yang login**
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Terapis hanya lihat terapi yang ditanganinya
        if request.user.role == 'terapis' and not request.user.is_superuser:
            return qs.filter(terapis=request.user)
        
        # Dokter lihat semua terapi
        if request.user.role == 'dokter':
            return qs
        
        # Admin lihat semua
        return qs