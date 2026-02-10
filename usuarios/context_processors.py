from django.urls import resolve, reverse
from equipos.models import Equipo
from usuarios.models import Usuario

def breadcrumbs(request):
    """
    Generar breadcrumbs dinámicos según la vista actual y la URL.
    """
    crumbs = [
        {"name": "Inicio", "url": reverse("landing")},
    ]

    try:
        resolver_match = resolve(request.path)
        view_name = resolver_match.url_name
        kwargs = resolver_match.kwargs

        # ---------- Nivel 1: sección ----------
        # if view_name in [
        #     "miperfil", "login", "signin", "logout",
        #     "eliminar_cuenta",
        #     "password_forget", "password_forget_done",
        #     "new_password", "new_password_done",
        #     "informacion_equipo"
        # ]:
        #     crumbs.append({
        #         "name": "Área privada",
        #         "url": "#"
        #     })

        # ---------- Nivel 2: páginas concretas ----------

        if view_name == "miperfil":
            crumbs.append({"name": "Mi perfil", "url": reverse("usuarios:miperfil")})

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

        elif view_name == "ver_perfil_usuario":
            slug = kwargs.get("slug")

            if slug:
                usuario = Usuario.objects.get(slug=slug)

                crumbs.append({
                    "name": "Usuarios",
                })

                crumbs.append({
                    "name": usuario.get_full_name(),
                    "url": reverse("usuarios:ver_perfil_usuario", args=[slug])
                })

        elif view_name == "informacion_equipo":
            slug = kwargs.get("slug")

            if slug:
                equipo = Equipo.objects.get(slug=slug)

                crumbs.append({
                    "name": "Equipos",
                })

                crumbs.append({
                    "name": equipo.nombre,   
                    "url": reverse("equipos:informacion_equipo", args=[slug])
                })

    except:
        # Si la URL no se resuelve correctamente, mostrar solo Inicio
        pass

    return {"breadcrumbs": crumbs}

