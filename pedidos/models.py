from django.db import models
import random
import string

def generar_codigo():
    """Genera código de 6 caracteres igual que el frontend."""
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return ''.join(random.choices(chars, k=6))

class Producto(models.Model):
    CATEGORIAS = [
        ('combina',    '🍱 Combina'),
        ('especial',   '🍲 Especial'),
        ('desayuno',   '☕ Desayuno'),
        ('bocadillos', '🥖 Bocadillos'),
        ('bebidas',    '☕ Cafés'),
    ]
    nombre    = models.CharField(max_length=150)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio    = models.DecimalField(max_digits=6, decimal_places=2)
    emoji     = models.CharField(max_length=10, default='🍽️')
    activo    = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return f"{self.emoji} {self.nombre} — {self.precio}€"


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente',   'Pendiente'),
        ('confirmado',  'Confirmado'),
        ('listo',       'Listo para recoger'),
        ('entregado',   'Entregado'),
        ('cancelado',   'Cancelado'),
    ]
    PAGO_CHOICES = [
        ('Establecimiento', 'Pago en Establecimiento'),
        ('Bizum',           'Bizum'),
    ]
    HORA_CHOICES = [
        ('11:15', 'Recreo (11:15)'),
        ('14:30', 'Salida (14:30)'),
    ]

    codigo       = models.CharField(max_length=6, unique=True, default=generar_codigo)
    nombre_alumno= models.CharField(max_length=100, blank=True, default='')
    metodo_pago  = models.CharField(max_length=20, choices=PAGO_CHOICES)
    hora_recogida= models.CharField(max_length=5, choices=HORA_CHOICES)
    total        = models.DecimalField(max_digits=8, decimal_places=2)
    estado       = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    creado_en    = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-creado_en']

    def __str__(self):
        return f"Pedido {self.codigo} — {self.hora_recogida} — {self.total}€"


class LineaPedido(models.Model):
    pedido    = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto  = models.ForeignKey(Producto, on_delete=models.PROTECT)
    opciones  = models.CharField(max_length=200, blank=True, default='')  # ej: "Solo + Tostada"
    precio    = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Línea de pedido'
        verbose_name_plural = 'Líneas de pedido'

    def __str__(self):
        return f"{self.producto.nombre} ({self.opciones}) — {self.precio}€"
