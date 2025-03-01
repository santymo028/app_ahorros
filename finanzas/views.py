from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AhorroForm, CompartirAhorroForm, AgregarPersonaForm, MovimientoForm
from .models import Ahorro, Movimiento, AhorroCompartido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    # Obtener los ahorros del usuario
    ahorros_personales = Ahorro.objects.filter(creado_por=request.user)
    ahorros_compartidos = Ahorro.objects.filter(compartido_con__usuario=request.user)
    
    # Obtener la lista de contactos (todos los usuarios excepto el actual)
    contactos = User.objects.exclude(id=request.user.id)
    contactos = Contacto.objects.filter(usuario=request.user)  # <--- Esto es clave
    
    return render(request, 'finanzas/lista_ahorros.html', {
        'ahorros_personales': ahorros_personales,
        'ahorros_compartidos': ahorros_compartidos,
        'contactos': contactos  # Sin coma al final
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
        return redirect('home')

    # Obtener los últimos 5 movimientos
    movimientos = Movimiento.objects.filter(ahorro=ahorro).order_by('-fecha')[:5]

    # Obtener la lista de usuarios con los que se comparte el ahorro
    usuarios_compartidos = AhorroCompartido.objects.filter(ahorro=ahorro).exclude(usuario=ahorro.creado_por)

    # Formulario para agregar personas al ahorro
    if request.method == 'POST' and 'agregar_persona' in request.POST:
        form_agregar_persona = AgregarPersonaForm(request.POST)
        if form_agregar_persona.is_valid():
            usuario = form_agregar_persona.cleaned_data['usuario']
            AhorroCompartido.objects.create(ahorro=ahorro, usuario=usuario)
            return redirect('detalle_ahorro', ahorro_id=ahorro.id)
    else:
        form_agregar_persona = AgregarPersonaForm()

    # Formulario para hacer movimientos
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
    
    # Lógica para eliminar un usuario compartido
    if request.method == 'POST' and 'eliminar_usuario' in request.POST:
        usuario_id = request.POST.get('usuario_id')
        if es_creador:
            AhorroCompartido.objects.filter(ahorro=ahorro, usuario_id=usuario_id).delete()
            return redirect('detalle_ahorro', ahorro_id=ahorro.id)

    return render(request, 'finanzas/detalle_ahorro.html', {
        'ahorro': ahorro,
        'movimientos': movimientos,
        'form_agregar_persona': form_agregar_persona,
        'form_movimiento': form_movimiento,
        'es_creador': es_creador,
        'es_compartido': es_compartido,
        'usuarios_compartidos': usuarios_compartidos,  # <--- Nueva variable
    })

@login_required
def profile(request):
    return redirect('home')

def inicio(request):
    if not User.objects.exists():  # Si no hay usuarios en la base de datos
        return redirect('registro')  # Redirige a la página de registro

    return render(request, 'inicio.html')  # Si hay usuarios, muestra la página normal


from .models import Contacto
from django.contrib import messages

@login_required
def agregar_contacto(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        try:
            contacto = User.objects.get(username=nombre_usuario)
            if not Contacto.objects.filter(usuario=request.user, contacto=contacto).exists():
                Contacto.objects.create(usuario=request.user, contacto=contacto)
                messages.success(request, f"{contacto.username} ha sido agregado a tus contactos.")
            else:
                messages.warning(request, f"{contacto.username} ya está en tu lista de contactos.")
        except User.DoesNotExist:
            messages.error(request, f"El usuario '{nombre_usuario}' no existe.")
        return redirect('home')


def eliminar_contacto(request, nombre_usuario):
    if request.method == 'POST':
        contacto = get_object_or_404(User, username=nombre_usuario)
        Contacto.objects.filter(usuario=request.user, contacto=contacto).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirige a la página principal después del registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})