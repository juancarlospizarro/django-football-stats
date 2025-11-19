from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name te permite usar 'namespaces' (ej: {% url 'usuarios:login' %})
app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('signin/', views.signin, name="signin"),

     # Recuperar contraseña
    path('forget_password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('forget_password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="usuarios/password_forget.html"
    ), name='password_reset_done'),

    # Nueva contraseña
    path('new_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="usuarios/new_password.html"
    ), name='password_reset_confirm'),
    path('new_password/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="usuarios/new_password.html"
    ), name='password_reset_complete'),
]