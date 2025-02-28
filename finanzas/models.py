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

class SolicitudRetiro(models.Model):
    ahorro = models.ForeignKey(Ahorro, on_delete=models.CASCADE, related_name='solicitudes_retiro')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_retiro')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(null=True, blank=True)  # None = Pendiente, True = Aprobado, False = Rechazado

    def __str__(self):
        estado = "Pendiente" if self.aprobado is None else "Aprobado" if self.aprobado else "Rechazado"
        return f"Retiro de {self.monto} por {self.usuario.username} - {estado}"
