from django.db import models
from django.utils import timezone
from apps.patients.models import Pasien
from apps.users.models import User


class Antrian(models.Model):
    """
    Model Antrian untuk mengelola waiting list dan antrian pasien
    Sesuai FR-06, FR-10
    """
    
    # Pilihan Status Antrian
    STATUS_CHOICES = (
        ('menunggu', 'Menunggu'),
        ('dipanggil', 'Dipanggil'),
        ('dalam_proses', 'Dalam Proses'),
        ('selesai', 'Selesai'),
        ('tidak_hadir', 'Tidak Hadir'),
        ('batal', 'Dibatalkan'),
    )
    
    # Pilihan Jenis Layanan
    JENIS_LAYANAN_CHOICES = (
        ('assessment', 'Assessment Medis'),
        ('terapi_wicara', 'Terapi Wicara'),
        ('terapi_okupasi', 'Terapi Okupasi'),
        ('terapi_fisik', 'Terapi Fisik'),
        ('terapi_perilaku', 'Terapi Perilaku'),
        ('konsultasi', 'Konsultasi'),
    )
    
    # Nomor Antrian - Generated otomatis
    nomor_antrian = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Nomor Antrian",
        help_text="Nomor antrian unik per hari",
        editable=False
    )
    
    # Relasi ke Pasien
    pasien = models.ForeignKey(
        Pasien,
        on_delete=models.CASCADE,
        related_name='antrian',
        verbose_name="Pasien"
    )
    
    # Jenis Layanan
    jenis_layanan = models.CharField(
        max_length=30,
        choices=JENIS_LAYANAN_CHOICES,
        verbose_name="Jenis Layanan"
    )
    
    # Status Antrian
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='menunggu',
        verbose_name="Status"
    )
    
    # Prioritas (untuk kasus tertentu)
    prioritas = models.CharField(
    max_length=10,
    choices=[
        ('normal', 'Normal'),
        ('prioritas', 'Prioritas'),
    ],
    default='normal',
    verbose_name="Prioritas"
)
    
    # Waktu
    tanggal_daftar = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Tanggal Pendaftaran"
    )
    
    tanggal_panggil = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Tanggal Dipanggil"
    )
    
    tanggal_mulai = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Tanggal Mulai Layanan"
    )
    
    tanggal_selesai = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Tanggal Selesai Layanan"
    )
    
    # Estimasi Waktu Tunggu (dalam menit)
    estimasi_waktu_tunggu = models.IntegerField(
        default=0,
        help_text="Estimasi waktu tunggu dalam menit",
        verbose_name="Estimasi Waktu Tunggu (menit)"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        verbose_name="Catatan"
    )
    
    # Admin/Dokter yang mengelola antrian
    dikelola_oleh = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='antrian_dikelola',
        verbose_name="Dikelola Oleh"
    )
    
    class Meta:
        db_table = 'antrian'
        verbose_name = 'Antrian'
        verbose_name_plural = 'Antrian'
        ordering = ['-tanggal_daftar']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['tanggal_daftar']),
            models.Index(fields=['pasien', 'status']),
        ]
    
    def __str__(self):
        return f"{self.nomor_antrian} - {self.pasien.nama_lengkap} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Generate nomor antrian otomatis jika belum ada"""
        if not self.nomor_antrian:
            today = timezone.now().strftime('%Y%m%d')
            # Hitung jumlah antrian hari ini
            jumlah_antrian = Antrian.objects.filter(
                tanggal_daftar__date=timezone.now().date()
            ).count() + 1
            
            # Format: A-YYYYMMDD-NNN
            self.nomor_antrian = f"A-{today}-{jumlah_antrian:03d}"
        
        super().save(*args, **kwargs)
    
    def panggil(self, dikelola_oleh=None):
        """Panggil pasien dari antrian"""
        self.status = 'dipanggil'
        self.tanggal_panggil = timezone.now()
        if dikelola_oleh:
            self.dikelola_oleh = dikelola_oleh
        self.save(update_fields=['status', 'tanggal_panggil', 'dikelola_oleh'])
    
    def mulai_layanan(self):
        """Mulai layanan untuk pasien"""
        self.status = 'dalam_proses'
        self.tanggal_mulai = timezone.now()
        self.save(update_fields=['status', 'tanggal_mulai'])
    
    def selesai_layanan(self):
        """Selesaikan layanan untuk pasien"""
        self.status = 'selesai'
        self.tanggal_selesai = timezone.now()
        self.save(update_fields=['status', 'tanggal_selesai'])
    
    @property
    def durasi_tunggu(self):
        """Hitung durasi waktu tunggu dalam menit"""
        if self.tanggal_panggil:
            delta = self.tanggal_panggil - self.tanggal_daftar
            return int(delta.total_seconds() / 60)
        return 0
    
    @property
    def durasi_layanan(self):
        """Hitung durasi layanan dalam menit"""
        if self.tanggal_selesai and self.tanggal_mulai:
            delta = self.tanggal_selesai - self.tanggal_mulai
            return int(delta.total_seconds() / 60)
        return 0


class LogNotifikasi(models.Model):
    """
    Model untuk mencatat log pengiriman notifikasi
    Sesuai FR-10 (Notifikasi Antrian)
    """
    
    # Metode Notifikasi
    METODE_CHOICES = (
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    )
    
    # Status Pengiriman
    STATUS_CHOICES = (
        ('terkirim', 'Terkirim'),
        ('gagal', 'Gagal'),
        ('pending', 'Pending'),
    )
    
    antrian = models.ForeignKey(
        Antrian,
        on_delete=models.CASCADE,
        related_name='log_notifikasi',
        verbose_name="Antrian"
    )
    
    metode = models.CharField(
        max_length=20,
        choices=METODE_CHOICES,
        verbose_name="Metode Notifikasi"
    )
    
    tujuan = models.CharField(
        max_length=100,
        verbose_name="Tujuan (Nomor HP/Email)"
    )
    
    pesan = models.TextField(
        verbose_name="Isi Pesan"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status Pengiriman"
    )
    
    tanggal_kirim = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Tanggal Kirim"
    )
    
    tanggal_dibaca = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Tanggal Dibaca"
    )
    
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Pesan Error (jika gagal)"
    )
    
    class Meta:
        db_table = 'log_notifikasi'
        verbose_name = 'Log Notifikasi'
        verbose_name_plural = 'Log Notifikasi'
        ordering = ['-tanggal_kirim']
    
    def __str__(self):
        return f"{self.metode} - {self.antrian.nomor_antrian} ({self.status})"