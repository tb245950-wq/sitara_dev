from django.db import models
from django.utils import timezone
from apps.patients.models import Pasien
from apps.users.models import User
from apps.assessments.models import AssessmentMedis


from django.core.exceptions import ValidationError

class Terapi(models.Model):
    NAMA_TERAPI_CHOICES = [
        ('terapi_wicara', 'Terapi Wicara'),
        ('terapi_okupasi', 'Terapi Okupasi'),
        ('terapi_fisik', 'Terapi Fisik'),
        ('terapi_perilaku', 'Terapi Perilaku'),
        ('terapi_sensori', 'Terapi Integrasi Sensori'),
        ('konsultasi', 'Konsultasi'),
    ]
    
    STATUS_CHOICES = [
        ('terjadwal', 'Terjadwal'),
        ('berjalan', 'Berjalan'),
        ('selesai', 'Selesai'),
        ('dibatalkan', 'Dibatalkan'),
    ]
    
    nama_terapi = models.CharField(
        max_length=100,
        choices=NAMA_TERAPI_CHOICES,
        verbose_name='Jenis Terapi'
    )
    deskripsi_terapi = models.TextField(
        blank=True,
        null=True,
        verbose_name='Deskripsi Terapi'
    )
    tanggal_mulai = models.DateField(verbose_name='Tanggal Mulai')
    tanggal_selesai = models.DateField(
        blank=True,
        null=True,
        verbose_name='Tanggal Selesai'
    )
    frekuensi = models.CharField(
        max_length=50,
        verbose_name='Frekuensi',
        help_text='Contoh: 2x seminggu'
    )
    durasi_per_sesi = models.IntegerField(
        default=60,
        verbose_name='Durasi per Sesi (menit)',
        help_text='Durasi setiap sesi dalam menit'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='terjadwal',
        verbose_name='Status'
    )
    catatan = models.TextField(
        blank=True,
        null=True,
        verbose_name='Catatan'
    )
    assessment = models.ForeignKey(
        AssessmentMedis,
        on_delete=models.PROTECT,
        related_name='terapi',
        verbose_name='Assessment Terkait'
    )
    pasien = models.ForeignKey(
        Pasien,
        on_delete=models.CASCADE,
        related_name='terapi',
        verbose_name='Pasien'
    )
    terapis = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='terapi_ditangani',
        limit_choices_to={'role': 'terapis'},
        verbose_name='Terapis'
    )
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)
    tanggal_diupdate = models.DateTimeField(auto_now=True)

    def clean(self):
        """Validasi integritas data sebelum simpan"""
        if self.assessment and self.assessment.status != 'selesai':
            raise ValidationError({
                'assessment': "Terapi hanya dapat dibuat dari Assessment yang sudah berstatus 'Selesai'."
            })
        
        # Pastikan pasien di Terapi sama dengan pasien di Assessment
        if self.assessment and self.pasien != self.assessment.pasien:
            raise ValidationError({
                'pasien': "Pasien pada Terapi harus sama dengan pasien pada Assessment terkait."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'terapi'
        verbose_name = 'Terapi'
        verbose_name_plural = 'Terapi'
        ordering = ['-tanggal_mulai']
        indexes = [
            models.Index(fields=['pasien', 'status']),
            models.Index(fields=['terapis']),
        ]


class MonitoringTerapi(models.Model):
    KEHADIRAN_CHOICES = [
        ('hadir', 'Hadir'),
        ('tidak_hadir', 'Tidak Hadir'),
        ('izin', 'Izin'),
    ]
    
    tanggal_sesi = models.DateTimeField(
        default=timezone.now,
        verbose_name='Tanggal Sesi'
    )
    durasi_aktual = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Durasi Aktual (menit)',
        help_text='Durasi aktual sesi dalam menit'
    )
    kehadiran = models.CharField(
        max_length=20,
        choices=KEHADIRAN_CHOICES,
        default='hadir',
        verbose_name='Kehadiran'
    )
    kondisi_pasien = models.TextField(verbose_name='Kondisi Pasien')
    catatan_perkembangan = models.TextField(verbose_name='Catatan Perkembangan')
    pencapaian_target = models.TextField(
        blank=True,
        null=True,
        verbose_name='Pencapaian Target'
    )
    rekomendasi_sesi_berikutnya = models.TextField(
        blank=True,
        null=True,
        verbose_name='Rekomendasi Sesi Berikutnya'
    )
    pasien = models.ForeignKey(
        Pasien,
        on_delete=models.CASCADE,
        related_name='monitoring_terapi',
        verbose_name='Pasien'
    )
    terapi = models.ForeignKey(
        Terapi,
        on_delete=models.CASCADE,
        related_name='monitoring',
        verbose_name='Terapi'
    )
    terapis = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='monitoring_dicatat',
        limit_choices_to={'role': 'terapis'},
        verbose_name='Terapis'
    )
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Pastikan pasien disinkronkan dari data Terapi induk"""
        if self.terapi:
            self.pasien = self.terapi.pasien
        super().save(*args, **kwargs)

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