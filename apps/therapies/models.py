from django.db import models
from django.utils import timezone
from apps.patients.models import Pasien
from apps.users.models import User
from apps.assessments.models import AssessmentMedis


class Terapi(models.Model):
    """
    Model Terapi untuk mencatat rencana dan pelaksanaan terapi
    Sesuai FR-08
    """
    
    # Status Terapi
    STATUS_CHOICES = (
        ('terjadwal', 'Terjadwal'),
        ('berjalan', 'Berjalan'),
        ('selesai', 'Selesai'),
        ('dibatalkan', 'Dibatalkan'),
    )
    
    # Jenis Terapi
    JENIS_TERAPI_CHOICES = (
        ('terapi_wicara', 'Terapi Wicara'),
        ('terapi_okupasi', 'Terapi Okupasi'),
        ('terapi_fisik', 'Terapi Fisik'),
        ('terapi_perilaku', 'Terapi Perilaku'),
        ('terapi_sensori', 'Terapi Integrasi Sensori'),
        ('konsultasi', 'Konsultasi'),
    )
    
    # Pasien
    pasien = models.ForeignKey(
        Pasien,
        on_delete=models.CASCADE,
        related_name='terapi',
        verbose_name="Pasien"
    )
    
    # Assessment terkait
    assessment = models.ForeignKey(
        AssessmentMedis,
        on_delete=models.PROTECT,
        related_name='terapi',
        verbose_name="Assessment Terkait"
    )
    
    # Terapis yang menangani
    terapis = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='terapi_ditangani',
        limit_choices_to={'role': 'terapis'},
        verbose_name="Terapis"
    )
    
    # Data Terapi
    nama_terapi = models.CharField(
        max_length=100,
        choices=JENIS_TERAPI_CHOICES,
        verbose_name="Jenis Terapi"
    )
    
    deskripsi_terapi = models.TextField(
        blank=True,
        null=True,
        verbose_name="Deskripsi Terapi"
    )
    
    # Jadwal
    tanggal_mulai = models.DateField(
        verbose_name="Tanggal Mulai"
    )
    
    tanggal_selesai = models.DateField(
        blank=True,
        null=True,
        verbose_name="Tanggal Selesai"
    )
    
    frekuensi = models.CharField(
        max_length=50,
        help_text="Contoh: 2x seminggu",
        verbose_name="Frekuensi"
    )
    
    durasi_per_sesi = models.IntegerField(
        default=60,
        help_text="Durasi setiap sesi dalam menit",
        verbose_name="Durasi per Sesi (menit)"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='terjadwal',
        verbose_name="Status"
    )
    
    # Catatan
    catatan = models.TextField(
        blank=True,
        null=True,
        verbose_name="Catatan"
    )
    
    # Metadata
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diupdate = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'terapi'
        verbose_name = 'Terapi'
        verbose_name_plural = 'Terapi'
        ordering = ['-tanggal_mulai']
        indexes = [
            models.Index(fields=['pasien', 'status']),
            models.Index(fields=['terapis']),
        ]
    
    def __str__(self):
        return f"{self.get_nama_terapi_display()} - {self.pasien.nama_lengkap}"


class MonitoringTerapi(models.Model):
    """
    Model Monitoring Terapi untuk mencatat perkembangan pasien setiap sesi
    Sesuai FR-09, FR-14
    """
    
    # Kehadiran
    KEHADIRAN_CHOICES = (
        ('hadir', 'Hadir'),
        ('tidak_hadir', 'Tidak Hadir'),
        ('izin', 'Izin'),
    )
    
    # Terapi terkait
    terapi = models.ForeignKey(
        Terapi,
        on_delete=models.CASCADE,
        related_name='monitoring',
        verbose_name="Terapi"
    )
    
    # Pasien (denormalisasi untuk kemudahan query)
    pasien = models.ForeignKey(
        Pasien,
        on_delete=models.CASCADE,
        related_name='monitoring_terapi',
        verbose_name="Pasien"
    )
    
    # Terapis yang mencatat
    terapis = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='monitoring_dicatat',
        limit_choices_to={'role': 'terapis'},
        verbose_name="Terapis"
    )
    
    # Data Sesi
    tanggal_sesi = models.DateTimeField(
        default=timezone.now,
        verbose_name="Tanggal Sesi"
    )
    
    durasi_aktual = models.IntegerField(
        blank=True,
        null=True,
        help_text="Durasi aktual sesi dalam menit",
        verbose_name="Durasi Aktual (menit)"
    )
    
    kehadiran = models.CharField(
        max_length=20,
        choices=KEHADIRAN_CHOICES,
        default='hadir',
        verbose_name="Kehadiran"
    )
    
    # Catatan Perkembangan
    kondisi_pasien = models.TextField(
        verbose_name="Kondisi Pasien"
    )
    
    catatan_perkembangan = models.TextField(
        verbose_name="Catatan Perkembangan"
    )
    
    pencapaian_target = models.TextField(
        blank=True,
        null=True,
        verbose_name="Pencapaian Target"
    )
    
    rekomendasi_sesi_berikutnya = models.TextField(
        blank=True,
        null=True,
        verbose_name="Rekomendasi Sesi Berikutnya"
    )
    
    # Metadata
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'monitoring_terapi'
        verbose_name = 'Monitoring Terapi'
        verbose_name_plural = 'Monitoring Terapi'
        ordering = ['-tanggal_sesi']
        indexes = [
            models.Index(fields=['pasien', 'tanggal_sesi']),
            models.Index(fields=['terapi']),
        ]
    
    def __str__(self):
        return f"Monitoring {self.pasien.nama_lengkap} - {self.tanggal_sesi.strftime('%d/%m/%Y')}"