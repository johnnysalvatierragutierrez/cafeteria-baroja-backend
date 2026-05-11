from django.urls import path
from . import views

urlpatterns = [
    # ── Catálogo público ──────────────────────────────────────────────────────
    path('productos/',                      views.ProductoListView.as_view(),       name='productos-list'),
    # ── Pedidos ───────────────────────────────────────────────────────────────
    path('pedidos/',                        views.PedidoCreateView.as_view(),       name='pedidos-create'),
    path('pedidos/<str:codigo>/',           views.PedidoDetalleView.as_view(),      name='pedidos-detalle'),
    # ── Panel admin ───────────────────────────────────────────────────────────
    path('admin/pedidos/',                  views.PedidoAdminListView.as_view(),    name='admin-pedidos'),
    path('admin/pedidos/<str:codigo>/estado/', views.PedidoEstadoView.as_view(),    name='admin-estado'),
    # ── Auth ──────────────────────────────────────────────────────────────────
    path('auth/login/',                     views.LoginView.as_view(),              name='auth-login'),
    path('auth/logout/',                    views.LogoutView.as_view(),             name='auth-logout'),
    path('auth/me/',                        views.MeView.as_view(),                 name='auth-me'),
]
