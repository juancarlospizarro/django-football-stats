from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende de AbstractUser.
    Sustituye al modelo auth.User por defecto de Django.
    """
    
    # Definimos los roles posibles
    class Rol(models.TextChoices):
        ADMIN = 'admin', _('Administrador')
        ENTRENADOR = 'entrenador', _('Entrenador')
        JUGADOR = 'jugador', _('Jugador')
        INVITADO = 'invitado', _('Invitado')

    # Campos adicionales comunes a todos los usuarios
    email = models.EmailField(_('dirección de correo electrónico'), unique=True)
    telefono = models.CharField(_('teléfono'), max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(_('fecha de nacimiento'), blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    
    rol = models.CharField(
        max_length=20, 
        choices=Rol.choices, 
        default=Rol.INVITADO
    )

    # Usamos el email como identificador principal en lugar del username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"


class PerfilJugador(models.Model):
    """
    Datos específicos para usuarios con rol de JUGADOR.
    """
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='perfil_jugador'
    )
    
    altura = models.PositiveIntegerField(_('altura (cm)'), null=True, blank=True)
    peso = models.DecimalField(_('peso (kg)'), max_digits=5, decimal_places=2, null=True, blank=True)
    dorsal = models.PositiveIntegerField(_('dorsal'), null=True, blank=True)
    
    class PiernaHabil(models.TextChoices):
        DERECHA = 'derecha', _('Derecha')
        IZQUIERDA = 'izquierda', _('Izquierda')
        AMBAS = 'ambas', _('Ambas')
        
    pierna_habil = models.CharField(
        max_length=10, 
        choices=PiernaHabil.choices, 
        default=PiernaHabil.DERECHA
    )
    
    # Campo para saber si es capitán
    es_capitan = models.BooleanField(_('es capitán'), default=False)

    def __str__(self):
        return f"Perfil Jugador: {self.usuario.get_full_name()}"


class PerfilEntrenador(models.Model):
    """
    Datos específicos para usuarios con rol de ENTRENADOR.
    """
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='perfil_entrenador'
    )
    
    # Ejemplo de campo específico: Licencia o Titulación
    licencia = models.CharField(_('número de licencia'), max_length=50, blank=True, null=True)
    experiencia_anos = models.PositiveIntegerField(_('años de experiencia'), default=0)

    def __str__(self):
        return f"Perfil Entrenador: {self.usuario.get_full_name()}"