from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),  # Ruta para la página de inicio
]

from .views import inicio, registro_usuario

urlpatterns = [
    path('', inicio, name='inicio'),  # Vista de inicio
    path('registro/', registro_usuario, name='registro'),  # Vista de registro
]