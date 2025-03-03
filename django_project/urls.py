"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from finanzas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.lista_ahorros, name='home'),  # Página principal
    path('crear-ahorro/', views.crear_ahorro, name='crear_ahorro'),
    path('detalle-ahorro/<int:ahorro_id>/', views.detalle_ahorro, name='detalle_ahorro'),
    path('compartir-ahorro/<int:ahorro_id>/', views.compartir_ahorro, name='compartir_ahorro'),
     path('logout/', auth_views.LogoutView.as_view(template_name='finanzas/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='finanzas/login.html'), name='login'),  # Iniciar sesión
    path('registro/', views.registro, name='registro'),
    path('accounts/profile/', views.profile, name='profile'),  # Nueva ruta para el perfil
    path('agregar_contacto/', views.agregar_contacto, name='agregar_contacto'),
    path('eliminar_contacto/<str:nombre_usuario>/', views.eliminar_contacto, name='eliminar_contacto'),
    path('rechazar_retiro/<int:solicitud_id>/', views.rechazar_retiro, name='rechazar_retiro'),
    path('solicitar_autorizacion/<int:ahorro_id>/', views.solicitar_autorizacion, name='solicitar_autorizacion'),
    path('autorizar_retiro/<int:solicitud_id>/', views.autorizar_retiro, name='autorizar_retiro'),
    path('rechazar_retiro/<int:solicitud_id>/', views.rechazar_retiro, name='rechazar_retiro'),
    path('marcar_notificacion_leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
]