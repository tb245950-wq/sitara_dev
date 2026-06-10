from django.db import models
from django.utils import timezone
from apps.users.models import User


class Laporan(models.Model):
    """
    Model Laporan untuk menyimpan metadata laporan operasional klinik
    Sesuai FR-11, FR-12, FR-15
    """
    
    # Tipe Laporan
    TIPE_LAPORAN_CHOICES = (
        ('harian', 'Laporan Harian'),
        ('mingguan', 'Laporan Mingguan'),
        ('bulanan', 'Laporan Bulanan'),
        ('evaluasi_pasien', 'Evaluasi Perkembangan Pasien'),
        ('statistik', 'Laporan Statistik'),
    )
    
    # Status Laporan
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('selesai', 'Selesai'),
        ('terkirim', 'Terkirim'),
    )
    
    # Pembuat Laporan
    dibuat_oleh = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='laporan_dibuat',
        verbose_name="Dibuat Oleh"
    )
    
    # Data Laporan
    tipe_laporan = models.CharField(
        max_length=30,
        choices=TIPE_LAPORAN_CHOICES,
        verbose_name="Tipe Laporan"
    )
    
    judul_laporan = models.CharField(
        max_length=200,
        verbose_name="Judul Laporan"
    )
    
    periode_mulai = models.DateField(
        verbose_name="Periode Mulai"
    )
    
    periode_selesai = models.DateField(
        verbose_name="Periode Selesai"
    )
    
    ringkasan_isi = models.TextField(
        verbose_name="Ringkasan Isi Laporan"
    )
    
    data_lengkap = models.JSONField(
        blank=True,
        null=True,
        help_text="Data lengkap laporan dalam format JSON",
        verbose_name="Data Lengkap"
    )
    
    # File Laporan
    file_pdf = models.FileField(
        upload_to='laporan/pdf/',
        blank=True,
        null=True,
        verbose_name="File PDF"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Status"
    )
    
    # Metadata
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diupdate = models.DateTimeField(auto_now=True)
    tanggal_dikirim = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Tanggal Dikirim"
    )
    
    class Meta:
        db_table = 'laporan'
        verbose_name = 'Laporan'
        verbose_name_plural = 'Laporan'
        ordering = ['-tanggal_dibuat']
        indexes = [
            models.Index(fields=['tipe_laporan', 'tanggal_dibuat']),
            models.Index(fields=['dibuat_oleh']),
        ]
    
    def __str__(self):
        return f"{self.judul_laporan} ({self.get_tipe_laporan_display()})"
    
    def tandai_selesai(self):
        """Tandai laporan sebagai selesai"""
        self.status = 'selesai'
        self.save(update_fields=['status', 'tanggal_diupdate'])
    
    def tandai_terkirim(self):
        """Tandai laporan sebagai terkirim"""
        self.status = 'terkirim'
        self.tanggal_dikirim = timezone.now()
        self.save(update_fields=['status', 'tanggal_dikirim', 'tanggal_diupdate'])