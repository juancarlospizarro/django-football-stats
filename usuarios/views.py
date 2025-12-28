from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Usuario, PerfilJugador, PerfilEntrenador

def login(request, user):
    return render(request, 'usuarios/login.html')

def signin(request):
    if request.method == "GET":
        return render(request, 'usuarios/signin.html')
    else:
        # 1. Obtener datos del formulario
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        fechanacimiento = request.POST.get('fechanacimiento')
        password_1 = request.POST.get('password1')
        password_2 = request.POST.get('password2')
        # Checkbox: Si está marcado devuelve 'true', si no devuelve None
        es_entrenador = request.POST.get('es_entrenador') 
        # Archivos: Las imágenes van en request.FILES, no en POST
        foto = request.FILES.get('foto') 

        # 2. Validaciones básicas
        if password_1 != password_2:
            return render(request, 'usuarios/signin.html', {'error': "Las contraseñas no coinciden."})
        
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'usuarios/signin.html', {'error': "Este correo electrónico ya está registrado."})

        # 3. Crear el Usuario
        try:
            # Usamos 'create_user' que se encarga de encriptar la contraseña automáticamente
            user = Usuario.objects.create_user(
                username=email, # Usamos el email como username interno
                first_name=nombre,
                last_name=apellidos,
                telefono=telefono,
                fecha_nacimiento=fechanacimiento,
                email=email,
                password=password_1,
                foto=foto # Guardamos la foto si la hay
            )

            # 4. Asignar Rol y Crear Perfil Específico
            if es_entrenador:
                user.rol = Usuario.Rol.ENTRENADOR
                # Creamos la ficha de entrenador vacía asociada a este usuario
                PerfilEntrenador.objects.create(usuario=user)
            else:
                user.rol = Usuario.Rol.JUGADOR
                # Creamos la ficha de jugador vacía asociada a este usuario
                PerfilJugador.objects.create(usuario=user)
            
            # Guardamos el cambio de rol
            user.save()

            # 5. Iniciar sesión automáticamente y redirigir
            login(request, user)
            
            # Redirigir a la página de inicio o dashboard
            return redirect('landing') 

        except Exception as e:
            # Si pasa algo raro, mostramos el error (útil en desarrollo)
            return render(request, 'usuarios/signin.html', {'error': f"Error al registrar: {str(e)}"})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usuarios/password_forget.html'
    email_template_name = 'usuarios/password_forget_email.html'
    subject_template_name = 'usuarios/password_forget_subject.txt'
    success_url = reverse_lazy('usuarios:password_forget_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "usuarios/new_password.html"
    success_url = reverse_lazy("usuarios:new_password_done")