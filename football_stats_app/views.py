from django.shortcuts import render, redirect

def landing(request):
    # 1. Si el usuario NO está logueado, mostramos la landing de invitado
    if not request.user.is_authenticated:
        return render(request, 'landing.html')

    # 2. Si el usuario SÍ está logueado, miramos quién es
    usuario = request.user

    # CASO A: Es un ADMIN (Superusuario)
    if usuario.is_superuser:
        return redirect('/admin/') 

    # CASO B: Es un ENTRENADOR
    elif usuario.rol == usuario.Rol.ENTRENADOR:
        if usuario.tiene_equipo:
            return render(request, 'usuarios/inicio_entrenador_con_equipo.html')
        else:
            return render(request, 'usuarios/inicio_entrenador_sin_equipo.html')

    # CASO C: Es un JUGADOR
    elif usuario.rol == usuario.Rol.JUGADOR:
        if usuario.tiene_equipo:
            return render(request, 'usuarios/inicio_jugador_con_equipo.html')
        else:
            return render(request, 'usuarios/inicio_jugador_sin_equipo.html')

    # CASO D: Rol desconocido o error
    else:
        return render(request, 'landing.html')