from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AhorroForm
from .forms import CompartirAhorroForm
from django.contrib.auth.decorators import login_required
from finanzas.models import Ahorro, Movimiento, AhorroCompartido
from finanzas.forms import AgregarPersonaForm, MovimientoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User

@login_required
def crear_ahorro(request):
    if request.method == 'POST':
        form = AhorroForm(request.POST)
        if form.is_valid():
            ahorro = form.save(commit=False)
            ahorro.creado_por = request.user
            ahorro.monto_actual = 0  # Inicializa el monto en 0
            ahorro.save()
            return redirect('home')
    else:
        form = AhorroForm()
    return render(request, 'finanzas/crear_ahorro.html', {'form': form})

@login_required
def lista_ahorros(request):
    ahorros_personales = Ahorro.objects.filter(creado_por=request.user)
    ahorros_compartidos = Ahorro.objects.filter(compartido_con__usuario=request.user)
    return render(request, 'finanzas/lista_ahorros.html', {
        'ahorros_personales': ahorros_personales,
        'ahorros_compartidos': ahorros_compartidos
    })

@login_required
def compartir_ahorro(request, ahorro_id):
    ahorro = get_object_or_404(Ahorro, id=ahorro_id, creado_por=request.user)
    if request.method == 'POST':
        form = CompartirAhorroForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            # Lógica para compartir el ahorro con el usuario
            return redirect('lista_ahorros')
    else:
        form = CompartirAhorroForm()
    return render(request, 'finanzas/compartir_ahorro.html', {'form': form, 'ahorro': ahorro})



@login_required
def detalle_ahorro(request, ahorro_id):
    ahorro = get_object_or_404(Ahorro, id=ahorro_id)
    
    # Verificar si el usuario es el creador o está compartido en el ahorro
    es_creador = ahorro.creado_por == request.user
    es_compartido = AhorroCompartido.objects.filter(ahorro=ahorro, usuario=request.user).exists()

    if not es_creador and not es_compartido:
        return redirect('home')  # Redirigir si el usuario no tiene acceso

    # Obtener los últimos 5 movimientos
    movimientos = Movimiento.objects.filter(ahorro=ahorro).order_by('-fecha')[:5]

    # Formulario para agregar personas al ahorro
    if request.method == 'POST' and 'agregar_persona' in request.POST:
        form_agregar_persona = AgregarPersonaForm(request.POST)
        if form_agregar_persona.is_valid():
            usuario = form_agregar_persona.cleaned_data['usuario']
            AhorroCompartido.objects.create(ahorro=ahorro, usuario=usuario)
            return redirect('detalle_ahorro', ahorro_id=ahorro.id)
    else:
        form_agregar_persona = AgregarPersonaForm()

    # Formulario para hacer consignaciones y retiros
    if request.method == 'POST' and 'hacer_movimiento' in request.POST:
        form_movimiento = MovimientoForm(request.POST)
        if form_movimiento.is_valid():
            movimiento = form_movimiento.save(commit=False)
            movimiento.ahorro = ahorro
            movimiento.save()
            # Actualizar el monto actual del ahorro
            if movimiento.tipo == 'consignacion':
                ahorro.monto_actual += movimiento.monto
            elif movimiento.tipo == 'retiro':
                ahorro.monto_actual -= movimiento.monto
            ahorro.save()
            return redirect('detalle_ahorro', ahorro_id=ahorro.id)
    else:
        form_movimiento = MovimientoForm()

    # Lógica para darse de baja o eliminar el ahorro
    if request.method == 'POST' and 'darse_de_baja' in request.POST:
        if es_compartido:
            AhorroCompartido.objects.filter(ahorro=ahorro, usuario=request.user).delete()
            return redirect('home')
    elif request.method == 'POST' and 'eliminar_ahorro' in request.POST:
        if es_creador:
            ahorro.delete()
            return redirect('home')

    return render(request, 'finanzas/detalle_ahorro.html', {
        'ahorro': ahorro,
        'movimientos': movimientos,
        'form_agregar_persona': form_agregar_persona,
        'form_movimiento': form_movimiento,
        'es_creador': es_creador,
        'es_compartido': es_compartido,
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'finanzas/registro.html', {'form': form})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return redirect('home') 

def inicio(request):
    if not User.objects.exists():  # Si no hay usuarios en la base de datos
        return redirect('registro')  # Redirige a la página de registro

    return render(request, 'inicio.html')  # Si hay usuarios, muestra la página normal