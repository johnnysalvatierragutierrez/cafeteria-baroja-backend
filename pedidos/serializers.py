from rest_framework import serializers
from .models import Producto, Pedido, LineaPedido


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'precio', 'emoji', 'activo']


class LineaPedidoInputSerializer(serializers.Serializer):
    """Lo que manda el frontend al crear pedido."""
    producto_id = serializers.IntegerField()
    opciones    = serializers.CharField(max_length=200, allow_blank=True, default='')
    precio      = serializers.DecimalField(max_digits=6, decimal_places=2)


class PedidoCreateSerializer(serializers.Serializer):
    nombre_alumno = serializers.CharField(max_length=100, allow_blank=True, default='')
    metodo_pago   = serializers.ChoiceField(choices=['Establecimiento', 'Bizum'])
    hora_recogida = serializers.ChoiceField(choices=['11:15', '14:30'])
    lineas        = LineaPedidoInputSerializer(many=True, min_length=1)

    def create(self, validated_data):
        lineas_data = validated_data.pop('lineas')
        total = sum(l['precio'] for l in lineas_data)
        pedido = Pedido.objects.create(total=total, **validated_data)
        for l in lineas_data:
            producto = Producto.objects.get(pk=l['producto_id'])
            LineaPedido.objects.create(
                pedido=pedido,
                producto=producto,
                opciones=l['opciones'],
                precio=l['precio'],
            )
        return pedido


class LineaPedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_emoji  = serializers.CharField(source='producto.emoji', read_only=True)

    class Meta:
        model = LineaPedido
        fields = ['id', 'producto_nombre', 'producto_emoji', 'opciones', 'precio']


class PedidoSerializer(serializers.ModelSerializer):
    lineas = LineaPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'codigo', 'nombre_alumno', 'metodo_pago',
            'hora_recogida', 'total', 'estado', 'creado_en', 'lineas',
        ]
