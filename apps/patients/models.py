from django.db import models
from django.utils import timezone
from datetime import date


from django.db import models, transaction
from django.utils import timezone
from datetime import date


class Pasien(models.Model):
    # ... (existing fields)

    def save(self, *args, **kwargs):
        """Generate NRM otomatis jika belum ada dengan locking agar thread-safe"""
        if not self.nrm:
            with transaction.atomic():
                tahun = timezone.now().year
                # Gunakan select_for_update() untuk mengunci baris saat menghitung
                # atau cara lain yang lebih robust untuk production skala besar
                jumlah_pasien = Pasien.objects.filter(
                    tanggal_registrasi__year=tahun
                ).select_for_update().count() + 1
                
                # Format NRM: YYYY-NNNNN (Tahun-Nomor Urut 5 digit)
                self.nrm = f"{tahun}-{jumlah_pasien:05d}"
                super().save(*args, **kwargs)
        else:
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