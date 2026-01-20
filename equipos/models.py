from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.utils.text import slugify

class Equipo(models.Model):
    """
    Modelo que representa a un Equipo de Fútbol.
    Atributos basados estrictamente en el diseño E/R proporcionado.
    """
    
    # 1. ID: Django crea automáticamente un campo 'id' (BigAuto) como clave primaria.
    # No hace falta escribirlo explícitamente.

    # 2. Nombre
    nombre = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Nombre del equipo"
    )

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    # Validador para asegurar que los colores sean códigos Hexadecimales (ej: #27a770)
    color_validator = RegexValidator(
        regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message='Introduce un código de color Hexadecimal válido (ej: #27a770)',
    )

    # 3. Color Principal
    color_principal = models.CharField(
        max_length=7, 
        default="#27a770", 
        validators=[color_validator],
        verbose_name="Color Principal"
    )
    
    # 4. Color Secundario
    color_secundario = models.CharField(
        max_length=7, 
        default="#504847", 
        validators=[color_validator],
        verbose_name="Color Secundario"
    )
    
    # 5. Dirección
    direccion = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Dirección completa"
    )

    # 6. Teléfono
    telefono = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        verbose_name="Teléfono de contacto"
    )

    # 7. Escudo (Requiere Pillow)
    escudo = models.ImageField(
        upload_to='escudos_equipos/', 
        blank=True, 
        null=True, 
        verbose_name="Escudo"
    )
    
    # 8. Año de Fundación
    anio_fundacion = models.PositiveIntegerField(
        verbose_name="Año de fundación",
        validators=[
            MinValueValidator(1850), 
            MaxValueValidator(timezone.now().year)
        ],
        help_text="Año en el que se fundó el club"
    )

    # Metadatos extra (opcional, pero recomendado)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
