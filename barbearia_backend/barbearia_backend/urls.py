from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/agendamentos/', include('agendamentos.urls')),
    path('api/pagamentos/', include('pagamentos.urls')),
]