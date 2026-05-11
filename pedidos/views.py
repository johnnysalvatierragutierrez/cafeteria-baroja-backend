from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from .models import Producto, Pedido
from .serializers import (
    ProductoSerializer, PedidoSerializer, PedidoCreateSerializer
)


# ── PRODUCTOS ─────────────────────────────────────────────────────────────────
class ProductoListView(generics.ListAPIView):
    """GET /api/productos/ — Devuelve todos los productos activos."""
    permission_classes = [AllowAny]
    serializer_class = ProductoSerializer

    def get_queryset(self):
        qs = Producto.objects.filter(activo=True)
        cat = self.request.query_params.get('categoria')
        if cat:
            qs = qs.filter(categoria=cat)
        return qs


# ── PEDIDOS ───────────────────────────────────────────────────────────────────
class PedidoCreateView(APIView):
    """POST /api/pedidos/ — Crea un pedido nuevo desde el frontend."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PedidoCreateSerializer(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()
            return Response(
                {
                    'codigo': pedido.codigo,
                    'total': str(pedido.total),
                    'hora_recogida': pedido.hora_recogida,
                    'metodo_pago': pedido.metodo_pago,
                    'estado': pedido.estado,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedidoDetalleView(generics.RetrieveAPIView):
    """GET /api/pedidos/<codigo>/ — Consulta un pedido por código."""
    permission_classes = [AllowAny]
    serializer_class = PedidoSerializer
    lookup_field = 'codigo'
    queryset = Pedido.objects.all()


# ── PANEL ADMIN: listado y cambio de estado ───────────────────────────────────
class PedidoAdminListView(generics.ListAPIView):
    """GET /api/admin/pedidos/ — Lista pedidos (requiere login)."""
    permission_classes = [IsAuthenticated]
    serializer_class = PedidoSerializer

    def get_queryset(self):
        qs = Pedido.objects.all()
        hora  = self.request.query_params.get('hora')
        estado = self.request.query_params.get('estado')
        if hora:
            qs = qs.filter(hora_recogida=hora)
        if estado:
            qs = qs.filter(estado=estado)
        return qs


class PedidoEstadoView(APIView):
    """PATCH /api/admin/pedidos/<codigo>/estado/ — Cambia estado del pedido."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, codigo):
        try:
            pedido = Pedido.objects.get(codigo=codigo)
        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)

        nuevo_estado = request.data.get('estado')
        estados_validos = [e[0] for e in Pedido.ESTADO_CHOICES]
        if nuevo_estado not in estados_validos:
            return Response({'error': f'Estado inválido. Opciones: {estados_validos}'}, status=400)

        pedido.estado = nuevo_estado
        pedido.save()
        return Response({'codigo': pedido.codigo, 'estado': pedido.estado})


# ── AUTENTICACIÓN ─────────────────────────────────────────────────────────────
class LoginView(APIView):
    """POST /api/auth/login/ — Login del administrador de cafetería."""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'mensaje': f'Bienvenido, {user.username}', 'es_staff': user.is_staff})
        return Response({'error': 'Credenciales incorrectas'}, status=401)


class LogoutView(APIView):
    """POST /api/auth/logout/ — Cierra sesión."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'mensaje': 'Sesión cerrada'})


class MeView(APIView):
    """GET /api/auth/me/ — Comprueba si hay sesión activa."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'es_staff': request.user.is_staff,
        })
