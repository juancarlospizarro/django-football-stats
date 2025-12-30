from django.contrib import admin
from .models import Usuario, PerfilJugador, PerfilEntrenador

admin.site.register(Usuario)
admin.site.register(PerfilJugador)
admin.site.register(PerfilEntrenador)
