from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.models import PerfilJugador, Usuario, PerfilEntrenador
from .models import Equipo, EquipoEntrenador, EquipoJugador

@login_required
def crear_equipo(request):

    usuario = request.user

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        anio_fundacion = request.POST.get("anio_fundacion")
        escudo = request.FILES.get("escudo")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        color_principal = request.POST.get("color_principal")
        color_secundario = request.POST.get("color_secundario")

        if not all([nombre, anio_fundacion, direccion, telefono]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("landing")

        equipo = Equipo(
            nombre=nombre,
            anio_fundacion=anio_fundacion,
            escudo=escudo,
            direccion=direccion,
            telefono=telefono,
            color_principal=color_principal,
            color_secundario=color_secundario
        )
        equipo.save()  # Esto ejecuta el método save() que genera el slug

        # Vincular al usuario como entrenador del equipo
        perfil_entrenador = PerfilEntrenador.objects.get_or_create(usuario=usuario)[0]
        EquipoEntrenador.objects.create(
            equipo=equipo,
            perfil_entrenador=perfil_entrenador
        )

        usuario.tiene_equipo = True
        usuario.save()

        messages.success(request, f"Equipo {equipo.nombre} creado correctamente.")

        # Recargar equipo para asegurar que tiene el slug
        equipo.refresh_from_db()
        return redirect('equipos:informacion_equipo', slug=equipo.slug)

    return render(request, "usuarios/inicio_entrenador_sin_equipo.html")

@login_required
def informacion_equipo(request, slug):
    equipo = get_object_or_404(Equipo, slug=slug)
    
    # Verificar si el usuario actual es entrenador de este equipo
    is_trainer = False
    if request.user.is_authenticated and request.user.rol == "entrenador":
        is_trainer = EquipoEntrenador.objects.filter(
            perfil_entrenador=request.user.perfil_entrenador,
            equipo=equipo,
            es_activo=True
        ).exists()
    
    # Obtener jugadores sin equipo
    jugadores_sin_equipo = PerfilJugador.objects.filter(
        usuario__tiene_equipo=False,
        usuario__rol='jugador'
    )
    
    # Obtener entrenador activo del equipo
    entrenador = equipo.entrenadores.filter(es_activo=True).first()
    
    # Obtener jugadores del equipo (activos)
    jugadores_equipo = equipo.jugadores.filter(es_activo=True).select_related(
        'perfil_jugador__usuario'
    ).order_by('perfil_jugador__usuario__first_name')
    
    context = {
        'equipo': equipo,
        'is_trainer': is_trainer,
        'jugadores_sin_equipo': jugadores_sin_equipo,
        'entrenador': entrenador,
        'jugadores_equipo': jugadores_equipo,
    }
    return render(request, 'equipos/informacion_equipo.html', context)

@login_required
def editar_jugador(request, jugador_id):
    try:
        perfil_jugador = get_object_or_404(PerfilJugador, id=jugador_id)
        
        # Verificar que el usuario es entrenador de algún equipo del jugador
        es_entrenador = False
        for equipo_jugador in perfil_jugador.equipos.filter(es_activo=True):
            es_entrenador = EquipoEntrenador.objects.filter(
                perfil_entrenador=request.user.perfil_entrenador,
                equipo=equipo_jugador.equipo,
                es_activo=True
            ).exists()
            if es_entrenador:
                break
        
        if not es_entrenador:
            return JsonResponse({'success': False, 'error': 'No tienes permiso'}, status=403)
        
        # Actualizar los datos
        dorsal = request.POST.get('dorsal')
        altura = request.POST.get('altura')
        peso = request.POST.get('peso')
        pierna_habil = request.POST.get('pierna_habil')
        es_capitan = request.POST.get('es_capitan') == 'on'
        
        if dorsal and dorsal.strip():
            perfil_jugador.dorsal = int(dorsal)
        if altura and altura.strip():
            perfil_jugador.altura = int(altura)
        if peso and peso.strip():
            perfil_jugador.peso = float(peso)
        if pierna_habil:
            perfil_jugador.pierna_habil = pierna_habil
        
        perfil_jugador.es_capitan = es_capitan
        perfil_jugador.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Información actualizada correctamente'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Vista AJAX para añadir jugador al equipo
@login_required
def agregar_jugador_equipo(request, equipo_id, jugador_id):
    if request.method == 'POST':
        equipo = get_object_or_404(Equipo, id=equipo_id)
        perfil_jugador = get_object_or_404(PerfilJugador, id=jugador_id)
        
        # Verificar que el usuario es entrenador de este equipo
        is_trainer = EquipoEntrenador.objects.filter(
            perfil_entrenador=request.user.perfil_entrenador,
            equipo=equipo,
            es_activo=True
        ).exists()
        
        if not is_trainer:
            return JsonResponse({'success': False, 'error': 'No tienes permiso'}, status=403)
        
        # Crear relación entre jugador y equipo
        equipo_jugador, created = EquipoJugador.objects.get_or_create(
            equipo=equipo,
            perfil_jugador=perfil_jugador
        )
        
        if created:
            # Actualizar el booleano tiene_equipo del usuario
            perfil_jugador.usuario.tiene_equipo = True
            perfil_jugador.usuario.save()
            
            return JsonResponse({
                'success': True,
                'message': f'{perfil_jugador.usuario.get_full_name()} añadido al equipo'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'El jugador ya está en este equipo'
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def listado_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, "equipos/listado.html", {"equipos": equipos})

@login_required
def editar_datos_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)

    if request.method == "POST":
        try:
            equipo.nombre = request.POST.get("nombre")
            equipo.anio_fundacion = request.POST.get("anio_fundacion")
            equipo.direccion = request.POST.get("direccion")
            equipo.telefono = request.POST.get("telefono")
            equipo.color_principal = request.POST.get("color_principal")
            equipo.color_secundario = request.POST.get("color_secundario")

            if "escudo" in request.FILES:
                equipo.escudo = request.FILES["escudo"]

            equipo.save()
            messages.success(request, "Datos del equipo actualizados correctamente")
            return redirect('equipos:informacion_equipo', slug=equipo.slug)

        except Exception as e:
            return render(request, 'equipos/informacion_equipo.html', {'equipo': equipo, 'error': f"Error al actualizar: {str(e)}"})

    return render(request, 'equipos/informacion_equipo.html', {'equipo': equipo})

@login_required
def eliminar_equipo(request, equipo_id):
    # Obtener el equipo y verificar que el usuario es el dueño (entrenador vinculado)
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    # Seguridad: Solo el entrenador del equipo puede borrarlo
    if request.user.perfil_entrenador.equipo != equipo:
        messages.error(request, "No tienes permiso para eliminar este equipo.")
        return redirect('landing')

    # # --- CONFIGURACIÓN DE ESTRATEGIA ---
    # # Pon esto en True para mantener histórico (Baja Lógica).
    # # Pon esto en False para borrar definitivamente (si ves que el histórico te complica).
    # GUARDAR_HISTORICO = False 

    # if request.method == 'POST':
    #     try:
    #         nombre_equipo = equipo.nombre
            
    #         # --- 1. NOTIFICAR A LOS JUGADORES (Común a ambas estrategias) ---
    #         # Obtenemos todos los jugadores del equipo antes de borrarlos/desvincularlos
    #         jugadores = equipo.jugadores.all().select_related('usuario')
            
    #         for perfil in jugadores:
    #             usuario_jugador = perfil.usuario
    #             if usuario_jugador.email:
    #                 asunto = f'Aviso: El equipo {nombre_equipo} ha sido disuelto'
    #                 mensaje = f"""
    #                 Hola {usuario_jugador.first_name},
                    
    #                 Te informamos que el entrenador ha eliminado el equipo "{nombre_equipo}".
                    
    #                 A partir de este momento, figuras en la plataforma como "Jugador sin equipo".
    #                 Tu historial y estadísticas personales se mantienen, pero ya no estás vinculado a este club.
                    
    #                 Atentamente,
    #                 El equipo de FutDataManager.
    #                 """
                    
    #                 # Enviamos el correo (fail_silently=True evita que si un correo falla, se pare todo el proceso)
    #                 try:
    #                     send_mail(
    #                         asunto,
    #                         mensaje,
    #                         settings.DEFAULT_FROM_EMAIL,
    #                         [usuario_jugador.email],
    #                         fail_silently=True
    #                     )
    #                 except Exception:
    #                     pass # Si falla un correo, seguimos borrando el equipo

    #         # --- 2. EJECUTAR EL BORRADO SEGÚN LA ESTRATEGIA ELEGIDA ---
    #         if GUARDAR_HISTORICO:
    #             # ESTRATEGIA A: Baja Lógica (Histórico)
    #             # Requiere que el modelo Equipo tenga el campo: activo = models.BooleanField(default=True)
    #             equipo.activo = False
    #             # Opcional: Renombrar para liberar el nombre único y permitir crear otro igual
    #             # equipo.nombre = f"{equipo.nombre} (Disuelto {equipo.id})" 
    #             equipo.save()
                
    #             # Desvinculamos a los jugadores manualmente (ya que no se borra el objeto padre)
    #             for perfil in jugadores:
    #                 perfil.equipo = None
    #                 perfil.save()
    #         else:
    #             # ESTRATEGIA B: Borrado Físico (Definitivo)
    #             # Al borrar el equipo, los jugadores se desvinculan solos gracias a on_delete=models.SET_NULL
    #             equipo.delete() 

    #         # --- 3. ACTUALIZAR AL ENTRENADOR (Común a ambas) ---
    #         request.user.tiene_equipo = False
    #         request.user.save()
            
    #         # Limpiamos la relación del perfil del entrenador
    #         request.user.perfil_entrenador.equipo = None
    #         request.user.perfil_entrenador.save()

    #         if GUARDAR_HISTORICO:
    #             messages.success(request, f'El equipo "{nombre_equipo}" ha sido archivado en el histórico.')
    #         else:
    #             messages.success(request, f'El equipo "{nombre_equipo}" ha sido eliminado definitivamente.')
            
    #     except Exception as e:
    #         messages.error(request, f"Ocurrió un error al procesar el equipo: {str(e)}")
            
    #     return redirect('landing')

    # return redirect('landing')
