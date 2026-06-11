from django.db import models
from django.utils import timezone
from datetime import date


class Pasien(models.Model):
    """
    Model Pasien untuk menyimpan data anak yang terdaftar di klinik
    Sesuai FR-03, FR-04, FR-05, FR-17
    """
    
    # Nomor Rekam Medis (NRM) - Generated otomatis
    nrm = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Nomor Rekam Medis",
        help_text="Nomor Rekam Medis unik pasien",
        editable=False
    )
    
    # Data Identitas Anak
    nama_lengkap = models.CharField(
        max_length=200,
        verbose_name="Nama Lengkap Anak"
    )
    
    nik = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="NIK Anak",
        help_text="Nomor Induk Kependudukan 16 digit"
    )
    
    tanggal_lahir = models.DateField(
        verbose_name="Tanggal Lahir"
    )
    
    jenis_kelamin = models.CharField(
        max_length=1,
        choices=[('L', 'Laki-laki'), ('P', 'Perempuan')],
        verbose_name="Jenis Kelamin"
    )
    
    tempat_lahir = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tempat Lahir"
    )
    
    # Data Orang Tua/Wali
    nama_wali = models.CharField(
        max_length=200,
        verbose_name="Nama Orang Tua/Wali"
    )
    
    nik_wali = models.CharField(
        max_length=16,
        verbose_name="NIK Orang Tua/Wali"
    )
    
    hubungan = models.CharField(
        max_length=20,
        choices=[
            ('Ayah', 'Ayah'),
            ('Ibu', 'Ibu'),
            ('Wali', 'Wali Lainnya')
        ],
        verbose_name="Hubungan dengan Anak"
    )
    
    nomor_telepon_wali = models.CharField(
        max_length=15,
        verbose_name="Nomor Telepon/WhatsApp Wali"
    )
    
    email_wali = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email Wali"
    )
    
    # Alamat
    alamat_lengkap = models.TextField(
        verbose_name="Alamat Lengkap"
    )
    
    rt_rw = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="RT/RW"
    )
    
    kelurahan = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Kelurahan"
    )
    
    kecamatan = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Kecamatan"
    )
    
    kota = models.CharField(
        max_length=100,
        default='Yogyakarta',
        verbose_name="Kota/Kabupaten"
    )
    
    provinsi = models.CharField(
        max_length=100,
        default='DI Yogyakarta',
        verbose_name="Provinsi"
    )
    
    # Informasi Tambahan
    golongan_darah = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('AB', 'AB'),
            ('O', 'O')
        ],
        verbose_name="Golongan Darah"
    )
    
    alergi = models.TextField(
        blank=True,
        null=True,
        help_text="Riwayat alergi (jika ada)"
    )
    
    # Status
    status_aktif = models.BooleanField(
        default=True,
        verbose_name="Status Aktif"
    )
    
    # Metadata
    tanggal_registrasi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Tanggal Registrasi"
    )
    
    tanggal_update_terakhir = models.DateTimeField(
        auto_now=True,
        verbose_name="Tanggal Update Terakhir"
    )
    
    class Meta:
        db_table = 'pasien'
        verbose_name = 'Pasien'
        verbose_name_plural = 'Pasien'
        ordering = ['nama_lengkap']
    
    def __str__(self):
        return f"{self.nrm} - {self.nama_lengkap}"
    
    def save(self, *args, **kwargs):
        """Generate NRM otomatis jika belum ada"""
        if not self.nrm:
            tahun = timezone.now().year
            # Hitung jumlah pasien di tahun ini
            jumlah_pasien = Pasien.objects.filter(
                tanggal_registrasi__year=tahun
            ).count() + 1
            
            # Format NRM: YYYY-NNNNN (Tahun-Nomor Urut 5 digit)
            self.nrm = f"{tahun}-{jumlah_pasien:05d}"
        
        super().save(*args, **kwargs)
    
    @property
    def usia(self):
        """Hitung usia pasien dalam tahun"""
        if not self.tanggal_lahir:
            return 0
        today = date.today()
        usia_tahun = today.year - self.tanggal_lahir.year - (
            (today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day)
        )
        return usia_tahun
    
    @property
    def usia_bulan(self):
        """Hitung usia pasien dalam bulan (untuk bayi/balita)"""
        if not self.tanggal_lahir:
            return 0
        today = date.today()
        usia_bulan = (today.year - self.tanggal_lahir.year) * 12 + (
            today.month - self.tanggal_lahir.month
        )
        return usia_bulan


class RiwayatKunjungan(models.Model):
    """
    Model untuk mencatat riwayat kunjungan pasien
    Sesuai FR-14 (Riwayat Rekam Medis)
    """
    
    pasien = models.ForeignKey(
        Pasien,
        on_delete=models.CASCADE,
        related_name='riwayat_kunjungan',
        verbose_name="Pasien"
    )
    
    tanggal_kunjungan = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Tanggal Kunjungan"
    )
    
    tujuan_kunjungan = models.CharField(
        max_length=200,
        verbose_name="Tujuan Kunjungan"
    )
    
    keterangan = models.TextField(
        blank=True,
        null=True,
        verbose_name="Keterangan"
    )
    
    class Meta:
        db_table = 'riwayat_kunjungan'
        verbose_name = 'Riwayat Kunjungan'
        verbose_name_plural = 'Riwayat Kunjungan'
        ordering = ['-tanggal_kunjungan']
    
    def __str__(self):
        return f"{self.pasien.nrm} - {self.tanggal_kunjungan.strftime('%d/%m/%Y')}"