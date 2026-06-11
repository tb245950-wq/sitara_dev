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
    
@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    # ... fieldsets dan list_display yang sudah ada ...
    
    # **RBAC: Pembatasan Aksi**
    def has_add_permission(self, request):
        # Admin dan Dokter yang bisa registrasi pasien baru
        return request.user.is_superuser or request.user.role in ['admin', 'dokter']
    
    def has_change_permission(self, request, obj=None):
        # Semua role authenticated bisa edit (tergantung kebijakan)
        return request.user.is_authenticated and request.user.is_active
    
    def has_delete_permission(self, request, obj=None):
        # Hanya Admin yang bisa hapus pasien
        return request.user.is_superuser or request.user.role == 'admin'
    
    def has_view_permission(self, request, obj=None):
        # Semua user login bisa lihat data pasien
        return request.user.is_authenticated