from django.contrib import admin
from .models import Producto, Pedido, LineaPedido


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ['producto', 'opciones', 'precio']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display  = ['codigo', 'nombre_alumno', 'hora_recogida', 'metodo_pago', 'total', 'estado', 'creado_en']
    list_filter   = ['estado', 'hora_recogida', 'metodo_pago']
    search_fields = ['codigo', 'nombre_alumno']
    readonly_fields = ['codigo', 'total', 'creado_en']
    inlines       = [LineaPedidoInline]
    list_editable = ['estado']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ['emoji', 'nombre', 'categoria', 'precio', 'activo']
    list_editable = ['precio', 'activo']
    list_filter   = ['categoria', 'activo']
