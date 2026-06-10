from django.contrib import admin
from .models import Pasien, RiwayatKunjungan


@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = ('nrm', 'nama_lengkap', 'nik', 'tanggal_lahir', 'usia', 'jenis_kelamin', 'nama_wali', 'nomor_telepon_wali', 'status_aktif')
    list_filter = ('jenis_kelamin', 'status_aktif', 'golongan_darah', 'tanggal_registrasi')
    search_fields = ('nrm', 'nama_lengkap', 'nik', 'nik_wali')
    readonly_fields = ('nrm', 'tanggal_registrasi', 'tanggal_update_terakhir', 'usia', 'usia_bulan')
    ordering = ('nama_lengkap',)
    
    fieldsets = (
        ('Nomor Rekam Medis', {'fields': ('nrm', 'status_aktif')}),
        ('Data Anak', {
            'fields': ('nama_lengkap', 'nik', 'tanggal_lahir', 'tempat_lahir', 'jenis_kelamin', 'golongan_darah', 'alergi')
        }),
        ('Data Orang Tua/Wali', {
            'fields': ('nama_wali', 'nik_wali', 'hubungan', 'nomor_telepon_wali', 'email_wali')
        }),
        ('Alamat Lengkap', {
            'fields': ('alamat_lengkap', 'rt_rw', 'kelurahan', 'kecamatan', 'kota', 'provinsi')
        }),
        ('Metadata', {
            'fields': ('tanggal_registrasi', 'tanggal_update_terakhir', 'usia', 'usia_bulan'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RiwayatKunjungan)
class RiwayatKunjunganAdmin(admin.ModelAdmin):
    list_display = ('pasien', 'tanggal_kunjungan', 'tujuan_kunjungan')
    list_filter = ('tanggal_kunjungan',)
    search_fields = ('pasien__nama_lengkap', 'pasien__nrm', 'tujuan_kunjungan')
    readonly_fields = ('tanggal_kunjungan',)
    ordering = ('-tanggal_kunjungan',)