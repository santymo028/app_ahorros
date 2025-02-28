from django import forms
from finanzas.models import Ahorro, AhorroCompartido, Movimiento
from django.contrib.auth.models import User

class AhorroForm(forms.ModelForm):
    class Meta:
        model = Ahorro
        fields = ['nombre', 'es_grupal']  # Excluye 'monto_actual' porque lo manejaremos manualmente

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializa el campo 'monto_actual' en 0 y hazlo no editable
        self.initial['monto_actual'] = 0
        self.fields['monto_actual'] = forms.DecimalField(
            initial=0,
            disabled=True,  # Hace que el campo no sea editable
            widget=forms.HiddenInput(),  # Oculta el campo en el formulario
        )

class CompartirAhorroForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = AhorroCompartido
        fields = ['usuario']


class CompartirAhorroForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = AhorroCompartido
        fields = ['usuario']

class AgregarPersonaForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = AhorroCompartido  # Si tienes un modelo para ahorros compartidos
        fields = ['usuario']

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'monto', 'descripcion']