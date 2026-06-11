from django.db import models
from django.utils import timezone
from apps.patients.models import Pasien
from apps.users.models import User
from apps.assessments.models import AssessmentMedis


from django.core.exceptions import ValidationError

class Terapi(models.Model):
    # ... (existing fields)

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
    # ... (existing fields)

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