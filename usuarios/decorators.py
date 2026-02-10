from django.core.exceptions import PermissionDenied
from usuarios.models import Usuario

def entrenador_o_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not (
            user.is_authenticated and
            (
                user.is_superuser or
                user.is_staff or
                user.rol == Usuario.Rol.ENTRENADOR
            )
        ):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper
