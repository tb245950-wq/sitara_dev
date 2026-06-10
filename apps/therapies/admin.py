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