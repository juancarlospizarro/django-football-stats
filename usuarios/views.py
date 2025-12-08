from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetConfirmView

def login(request):
    return render(request, 'usuarios/login.html')

def signin(request):
    if request.method == "GET":
        return render(request, 'usuarios/signin.html')
    else:
        if request.POST["password1"] != request.POST["password2"]:
            return render(request, 'usuarios/signin.html', {'error': "Las contraseñas no coinciden."})
        


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usuarios/password_forget.html'
    email_template_name = 'usuarios/password_forget_email.html'
    subject_template_name = 'usuarios/password_forget_subject.txt'
    success_url = reverse_lazy('usuarios:password_forget_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "usuarios/new_password.html"
    success_url = reverse_lazy("usuarios:new_password_done")