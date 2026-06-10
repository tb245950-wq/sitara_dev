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