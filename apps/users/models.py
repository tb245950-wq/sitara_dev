from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Model User untuk menyimpan data seluruh pengguna sistem
    (Admin, Dokter, dan Terapis) dengan Role-Based Access Control
    Sesuai FR-01, FR-13, FR-18 dan Bab 2.3 Karakteristik Pengguna
    """
    
    # Pilihan Role (Sesuai Bab 2.3 Karakteristik Pengguna)
    ROLE_CHOICES = (
        ('admin', 'Admin Klinik'),
        ('dokter', 'Dokter/Tenaga Medis'),
        ('terapis', 'Terapis'),
    )
    
    # Override groups dan user_permissions dengan related_name unik
    # untuk menghindari konflik dengan auth.User default
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sitara_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sitara_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    # Field untuk Role-Based Access Control (RBAC) - NFR-06
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='admin',
        help_text="Role pengguna untuk RBAC"
    )
    
    # Informasi tambahan untuk tenaga medis (Dokter & Terapis)
    spesialisasi = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Spesialisasi (untuk Dokter dan Terapis)"
    )
    
    nomor_str = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Nomor STR/SIP",
        help_text="Nomor Surat Tanda Registrasi (untuk Dokter/Terapis)"
    )
    
    nomor_telepon = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Nomor telepon yang dapat dihubungi"
    )
    
    foto_profil = models.ImageField(
        upload_to='users/foto_profil/',
        blank=True,
        null=True,
        help_text="Foto profil pengguna"
    )
    
    # Metadata untuk audit trail (NFR-07)
    tanggal_dibuat = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Tanggal Dibuat"
    )
    
    tanggal_terakhir_login = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name="Tanggal Terakhir Login"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Menandakan apakah akun masih aktif"
    )
    
    class Meta:
        db_table = 'pengguna'
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Pengguna'
        ordering = ['username']
    
    def __str__(self):
        role_display = dict(self.ROLE_CHOICES).get(self.role, self.role)
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({role_display})"
        return f"{self.username} ({role_display})"
    
    def update_last_login(self):
        """Update tanggal terakhir login"""
        self.tanggal_terakhir_login = timezone.now()
        self.save(update_fields=['tanggal_terakhir_login'])
    
    @property
    def is_admin(self):
        """Cek apakah user adalah admin"""
        return self.role == 'admin'
    
    @property
    def is_dokter(self):
        """Cek apakah user adalah dokter"""
        return self.role == 'dokter'
    
    @property
    def is_terapis(self):
        """Cek apakah user adalah terapis"""
        return self.role == 'terapis'
    
    def get_role_display_name(self):
        """Mendapatkan nama role yang mudah dibaca"""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)