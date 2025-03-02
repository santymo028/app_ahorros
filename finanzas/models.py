from django.db import models
from django.contrib.auth.models import User

class Ahorro(models.Model):
    nombre = models.CharField(max_length=100)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ahorros_creados', null=True, blank=True)
    es_grupal = models.BooleanField(default=False)
    miembros = models.ManyToManyField(User, related_name='ahorros', blank=True)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('consignacion', 'Consignación'),
        ('retiro', 'Retiro'),
    ]
    
    ahorro = models.ForeignKey(Ahorro, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=12, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} de {self.monto} en {self.ahorro.nombre}"

class AhorroCompartido(models.Model):
    ahorro = models.ForeignKey(Ahorro, on_delete=models.CASCADE, related_name='compartido_con')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ahorros_compartidos')
    fecha_compartido = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ahorro', 'usuario'], name='unique_ahorro_usuario')
        ]

    def __str__(self):
        return f"{self.ahorro.nombre} compartido con {self.usuario.username}"

class SolicitudAutorizacion(models.Model):
    ahorro = models.ForeignKey(Ahorro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.usuario.username} para retirar ${self.monto} de {self.ahorro.nombre}"

    
class Contacto(models.Model):
    usuario = models.ForeignKey(User, related_name='contactos_agregados', on_delete=models.CASCADE)
    contacto = models.ForeignKey(User, related_name='contactos_agregados_por', on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contacto.username} (Agregado por {self.usuario.username})"