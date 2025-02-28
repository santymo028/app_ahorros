from django.contrib import admin
from .models import Ahorro

@admin.register(Ahorro)
class AhorroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'monto_actual', 'creado_por', 'es_grupal']  # Excluye 'descripcion' y 'fecha_creacion'
    list_filter = ['es_grupal']
    search_fields = ['nombre']