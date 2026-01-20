from django.urls import path
from . import views

app_name = 'equipos'

urlpatterns = [
    path("crear_equipo/", views.crear_equipo, name='crear_equipo'),
    path('<slug:slug>/', views.informacion_equipo, name='informacion_equipo'),
    path('listado_equipos/', views.listado_equipos, name='listado_equipos')
]