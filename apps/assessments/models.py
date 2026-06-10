from django.db import models
from django.utils import timezone
from apps.patients.models import Pasien
from apps.users.models import User
from apps.queues.models import Antrian


class AssessmentMedis(models.Model):
    """
    Model Assessment Medis untuk menyimpan hasil pemeriksaan dokter
    Sesuai FR-07, FR-14
    """
    
    # Status Assessment
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('selesai', 'Selesai'),
        ('dirujuk', 'Dirujuk'),
    )
    
    # Pasien yang di-assess
    pasien = models.ForeignKey(
        Pasien,
        on_delete=models.CASCADE,
        related_name='assessments',
        verbose_name="Pasien"
    )
    
    # Dokter yang melakukan assessment
    dokter = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assessments_dilakukan',
        limit_choices_to={'role': 'dokter'},
        verbose_name="Dokter"
    )
    
    # Antrian terkait (opsional)
    antrian = models.ForeignKey(
        Antrian,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assessments',
        verbose_name="Antrian Terkait"
    )
    
    # Tanggal Assessment
    tanggal_assessment = models.DateTimeField(
        default=timezone.now,
        verbose_name="Tanggal Assessment"
    )
    
    # Data Assessment
    keluhan_utama = models.TextField(
        verbose_name="Keluhan Utama"
    )
    
    riwayat_penyakit = models.TextField(
        blank=True,
        null=True,
        verbose_name="Riwayat Penyakit"
    )
    
    hasil_pemeriksaan = models.TextField(
        verbose_name="Hasil Pemeriksaan Fisik"
    )
    
    diagnosis = models.TextField(
        verbose_name="Diagnosis"
    )
    
    catatan_medis = models.TextField(
        blank=True,
        null=True,
        verbose_name="Catatan Medis Tambahan"
    )
    
    # Rencana Terapi
    rencana_terapi = models.TextField(
        verbose_name="Rencana Terapi"
    )
    
    frekuensi_terapi = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Contoh: 2x seminggu, 3x sebulan",
        verbose_name="Frekuensi Terapi"
    )
    
    durasi_terapi = models.IntegerField(
        blank=True,
        null=True,
        help_text="Durasi terapi dalam minggu/bulan",
        verbose_name="Durasi Terapi (minggu)"
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
    
    class Meta:
        db_table = 'assessment_medis'
        verbose_name = 'Assessment Medis'
        verbose_name_plural = 'Assessment Medis'
        ordering = ['-tanggal_assessment']
        indexes = [
            models.Index(fields=['pasien', 'tanggal_assessment']),
            models.Index(fields=['dokter']),
        ]
    
    def __str__(self):
        return f"Assessment {self.pasien.nama_lengkap} - {self.tanggal_assessment.strftime('%d/%m/%Y')}"
    
    def selesai_assessment(self):
        """Tandai assessment sebagai selesai"""
        self.status = 'selesai'
        self.save(update_fields=['status', 'tanggal_diupdate'])