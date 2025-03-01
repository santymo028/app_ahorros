from django.contrib import admin
from .models import Ahorro
from .models import Contacto  # Importa el modelo Contacto

@admin.register(Ahorro)
class AhorroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'monto_actual', 'creado_por', 'es_grupal']  # Excluye 'descripcion' y 'fecha_creacion'
    list_filter = ['es_grupal']
    search_fields = ['nombre']
    
# Registra el modelo Contacto en el panel de administración
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contacto', 'fecha_agregado')  # Campos que se mostrarán en la lista
    list_filter = ('usuario', 'contacto')  # Filtros para facilitar la búsqueda
    search_fields = ('usuario__username', 'contacto__username')  # Campos de búsqueda