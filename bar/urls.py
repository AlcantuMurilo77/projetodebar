from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('delivery/', include('delivery.urls')),
    path('cozinha/', include('cozinha.urls')),
]