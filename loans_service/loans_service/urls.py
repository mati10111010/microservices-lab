from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    # Aquí se incluye el archivo urls.py de la aplicación 'loans_app'
    path('api/', include('loans_app.urls')), 
    # De esta forma, el endpoint será /api/loans/
]