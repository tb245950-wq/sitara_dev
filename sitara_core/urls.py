from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin (sesuai FR-13)
    path('admin/', admin.site.urls),
    
    # SITARA Apps URLs (akan ditambahkan nanti)
    # path('pasien/', include('apps.patients.urls')),
    # path('antrian/', include('apps.queues.urls')),
    # path('assessment/', include('apps.assessments.urls')),
    # path('terapi/', include('apps.therapies.urls')),
    # path('laporan/', include('apps.reports.urls')),
    
    # Redirect root ke admin (sementara)
    path('', admin.site.urls),
]

# Serve media files di development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)