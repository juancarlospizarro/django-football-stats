from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class AdminAccessMiddleware:
    """Middleware que valida el acceso al panel de administración"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Si intenta acceder a /admin/
        if request.path.startswith('/admin/'):
            # Si no está autenticado, lo redirige al login
            if not request.user.is_authenticated:
                return redirect('login')
            # Si está autenticado pero no es superuser, lanza error 403
            elif not request.user.is_superuser:
                raise PermissionDenied("No tienes permiso para acceder al panel de administración")
        
        response = self.get_response(request)
        return response
