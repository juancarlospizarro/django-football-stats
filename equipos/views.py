from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.models import Usuario
from .models import Equipo

@login_required
def crear_equipo(request):

    usuario = request.user
    
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.POST.get("nombre")
        anio_fundacion = request.POST.get("anio_fundacion")
        escudo = request.FILES.get("escudo")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        color_principal = request.POST.get("color_principal")
        color_secundario = request.POST.get("color_secundario")

        # Validaciones
        if not nombre or not anio_fundacion or not direccion or not telefono or not color_principal or not color_secundario:
            messages.error(request, "El nombre y el año de fundación son obligatorios.")
            return redirect("landing")

        # Crear el equipo
        equipo = Equipo.objects.create(
            nombre=nombre,
            anio_fundacion=anio_fundacion,
            escudo=escudo,
            direccion=direccion,
            telefono=telefono,
            color_principal=color_principal,
            color_secundario=color_secundario
        )

        usuario.tiene_equipo = True
        usuario.save()

        messages.success(request, f"Equipo '{equipo.nombre}' creado correctamente.")
        return render(request, "usuarios/inicio_entrenador_sin_equipo.html")

    return redirect("landing")

@login_required
def informacion_equipo(request, slug):
    equipo = get_object_or_404(Equipo, slug=slug)
    return render(request, 'equipos/informacion_equipo.html', {'equipo': equipo})

@login_required
def listado_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, "equipos/listado.html", {"equipos": equipos})
