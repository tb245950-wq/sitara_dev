from django.db import models
from django.utils import timezone
from apps.patients.models import Pasien
from apps.users.models import User


from django.db import models, transaction
from django.utils import timezone
from apps.patients.models import Pasien
from apps.users.models import User


class Antrian(models.Model):
    # ... (existing fields)

    def save(self, *args, **kwargs):
        """Generate nomor antrian otomatis jika belum ada dengan locking"""
        if not self.nomor_antrian:
            with transaction.atomic():
                today_date = timezone.now().date()
                today_str = timezone.now().strftime('%Y%m%d')
                
                # Gunakan select_for_update untuk mencegah tabrakan nomor antrian
                jumlah_antrian = Antrian.objects.filter(
                    tanggal_daftar__date=today_date
                ).select_for_update().count() + 1
                
                # Format: A-YYYYMMDD-NNN
                self.nomor_antrian = f"A-{today_str}-{jumlah_antrian:03d}"
                super().save(*args, **kwargs)
        else:
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