from django.urls import path
from . import views

app_name = 'equipos'

urlpatterns = [
    path("crear_equipo/", views.crear_equipo, name='crear_equipo'),
    path('listado_equipos/', views.listado_equipos, name='listado_equipos'),
    path('api/agregar-jugador/<int:equipo_id>/<int:jugador_id>/', views.agregar_jugador_equipo, name='agregar_jugador_equipo'),
    path('api/editar-jugador/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('<slug:slug>/', views.informacion_equipo, name='informacion_equipo'),
]