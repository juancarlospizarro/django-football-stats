from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Usuario, PerfilJugador, PerfilEntrenador
from django.http import JsonResponse
from django.contrib import messages

def login_view(request):
    if request.method == "GET":
        return render(request, 'usuarios/login.html')

    # POST → procesar login
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Autenticación
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "Sesión inciada correctamente.")
        return render(request, "usuarios/login.html")  # o dashboard
    else:
        return render(request, 'usuarios/login.html', {'error': "El usuario no existe o la contraseña es incorrecta.", "email_value": email})

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
            return render(request, 'usuarios/signin.html', {'error': "Las contraseñas no coinciden.", 'nombre_value': nombre, 'apellidos_value': apellidos, 'telefono_value': telefono, 'email_value': email, 'fechanacimiento_value': fechanacimiento, 'es_entrenador_value': es_entrenador, 'foto_value': foto})
        
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'usuarios/signin.html', {'error': "Este correo electrónico ya está registrado.", 'nombre_value': nombre, 'apellidos_value': apellidos, 'telefono_value': telefono, 'email_value': email, 'fechanacimiento_value': fechanacimiento, 'es_entrenador_value': es_entrenador, 'foto_value': foto})

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
            messages.success(request, "Te has registrado correctamente")
            # Redirigir a la página de inicio o dashboard
            return render(request, "usuarios/signin.html")

        except Exception as e:
            # Si pasa algo raro, mostramos el error (útil en desarrollo)
            return render(request, 'usuarios/signin.html', {'error': f"Error al registrar: {str(e)}"})

def logout_view(request):
    logout(request)
    return redirect('landing')  # o 'usuarios:login'

def miperfil(request):
    return render(request, 'usuarios/miperfil.html')

def eliminar_cuenta(request):
    if request.method == "POST":
        user = request.user
        logout(request)          # cerrar sesión primero
        user.delete()            # eliminar usuario
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usuarios/password_forget.html'
    email_template_name = 'usuarios/password_forget_email.html'
    subject_template_name = 'usuarios/password_forget_subject.txt'
    success_url = reverse_lazy('usuarios:password_forget_done')
    html_email_template_name = 'usuarios/password_forget_email.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "usuarios/new_password.html"
    success_url = reverse_lazy("usuarios:new_password_done")