from django.urls import path
from . import views

# app_name te permite usar 'namespaces' (ej: {% url 'usuarios:login' %})
app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('signin/', views.signin, name="signin"),
    path('forget_password/', views.password_forget, name="password_forget"),
    path('new_password/', views.new_password, name="new_password")
]