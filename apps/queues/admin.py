from django.contrib import admin
from django.utils.html import format_html
from .models import Antrian, LogNotifikasi


@admin.register(Antrian)
class AntrianAdmin(admin.ModelAdmin):
    list_display = ('nomor_antrian', 'pasien', 'jenis_layanan', 'status', 'prioritas', 'tanggal_daftar', 'dikelola_oleh')
    list_filter = ('status', 'jenis_layanan', 'prioritas', 'tanggal_daftar')
    search_fields = ('nomor_antrian', 'pasien__nama_lengkap', 'pasien__nrm')
    readonly_fields = ('nomor_antrian', 'tanggal_daftar', 'durasi_tunggu', 'durasi_layanan')
    ordering = ('-tanggal_daftar',)
    list_editable = ('status',)
    
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
        ('Statistik', {
            'fields': ('durasi_tunggu', 'durasi_layanan'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LogNotifikasi)
class LogNotifikasiAdmin(admin.ModelAdmin):
    list_display = ('antrian', 'metode', 'tujuan', 'status', 'tanggal_kirim')
    list_filter = ('metode', 'status', 'tanggal_kirim')
    search_fields = ('antrian__nomor_antrian', 'tujuan', 'pesan')
    readonly_fields = ('tanggal_kirim',)
    ordering = ('-tanggal_kirim',)