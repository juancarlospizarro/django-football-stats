# usuarios/urls.py
from django.urls import path
from .views import ResetPasswordView, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('signin/', views.signin, name="signin"),

    # Enviar email
    path('password_forget/', 
         ResetPasswordView.as_view(), 
         name='password_forget'),

    # Email enviado
    path('password_forget/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="usuarios/password_forget_done.html"),
         name='password_forget_done'),

    # Confirmar contraseña
    path('new_password/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='new_password'),

    # Contraseña cambiada
    path('new_password/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="usuarios/new_password_done.html"),
         name='new_password_done'),
]
