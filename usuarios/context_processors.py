from django.urls import resolve, reverse

def breadcrumbs(request):
    """
    Genera breadcrumbs dinámicos según la vista actual y la URL.
    """
    crumbs = [
        {"name": "Inicio", "url": reverse("landing")},
    ]

    try:
        resolver_match = resolve(request.path)
        view_name = resolver_match.url_name
        kwargs = resolver_match.kwargs

        # Perfil general
        if view_name == "miperfil":
            crumbs.append({"name": "Mi perfil", "url": reverse("usuarios:miperfil")})

        # Otras vistas ejemplo
        elif view_name == "login":
            crumbs.append({"name": "Iniciar sesión", "url": reverse("usuarios:login")})

        elif view_name == "signin":
            crumbs.append({"name": "Registrarse", "url": reverse("usuarios:signin")})

        elif view_name == "logout":
            crumbs.append({"name": "Cerrar sesión", "url": reverse("usuarios:logout")})

        elif view_name == "eliminar_cuenta":
            crumbs.append({"name": "Eliminar cuenta", "url": reverse("usuarios:eliminar_cuenta")})

        elif view_name == "password_forget":
            crumbs.append({"name": "Restablecer contraseña", "url": reverse("usuarios:password_forget")})

        elif view_name == "password_forget_done":
            crumbs.append({"name": "Restablecer contraseña", "url": reverse("usuarios:password_forget_done")})

        elif view_name == "new_password":
            crumbs.append({"name": "Nueva contraseña", "url": reverse("usuarios:new_password")})

        elif view_name == "new_password_done":
            crumbs.append({"name": "Nueva contraseña", "url": reverse("usuarios:new_password_done")})

    except:
        # Si la URL no se resuelve correctamente, mostrar solo Inicio
        pass

    return {"breadcrumbs": crumbs}
