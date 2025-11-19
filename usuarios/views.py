from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

def login(request):
    return render(request, 'usuarios/login.html')

def signin(request):
    return render(request, 'usuarios/signin.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usuarios/password_forget.html'
    email_template_name = 'usuarios/password_forget_email.html'
    subject_template_name = 'usuarios/password_forget_subject.txt'
    success_url = reverse_lazy('usuarios:password_reset_done')
