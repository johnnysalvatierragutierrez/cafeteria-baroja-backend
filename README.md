# 🍱 Backend — Cafetería Baroja

Backend Django + MySQL para la app de pedidos de la cafetería del IES Pío Baroja.

---

## 🚀 Instalación paso a paso

### 1. Crea el entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Instala dependencias
```bash
pip install -r requirements.txt
```

### 3. Crea la base de datos en MySQL
```bash
mysql -u root -p < crear_base_datos.sql
```

### 4. Configura la conexión en `cafeteria_baroja/settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cafeteria_baroja_db',
        'USER': 'cafeteria_user',        # o 'root'
        'PASSWORD': 'cafeteria2024',     # tu contraseña
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Crea las tablas
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Carga los productos del menú
```bash
python manage.py loaddata pedidos/fixtures/productos_iniciales.json
```

### 7. Crea el usuario administrador
```bash
python manage.py createsuperuser
```

### 8. Arranca el servidor
```bash
python manage.py runserver
```

---

## 📡 Endpoints de la API

| Método | URL | Descripción | Auth |
|--------|-----|-------------|------|
| GET | `/api/productos/` | Lista todos los productos activos | ❌ |
| GET | `/api/productos/?categoria=combina` | Filtra por categoría | ❌ |
| POST | `/api/pedidos/` | Crea un pedido nuevo | ❌ |
| GET | `/api/pedidos/<codigo>/` | Consulta un pedido por código | ❌ |
| GET | `/api/admin/pedidos/` | Lista pedidos (panel admin) | ✅ |
| PATCH | `/api/admin/pedidos/<codigo>/estado/` | Cambia estado del pedido | ✅ |
| POST | `/api/auth/login/` | Login administrador | ❌ |
| POST | `/api/auth/logout/` | Logout | ✅ |
| GET | `/api/auth/me/` | Sesión activa | ✅ |
| GET | `/django-admin/` | Panel admin Django | ✅ |

---

## 📦 Ejemplo: crear pedido desde el frontend

```json
POST /api/pedidos/
{
  "nombre_alumno": "María García",
  "metodo_pago": "Bizum",
  "hora_recogida": "11:15",
  "lineas": [
    {"producto_id": 1, "opciones": "", "precio": 7.80},
    {"producto_id": 12, "opciones": "Solo", "precio": 1.40}
  ]
}
```

**Respuesta:**
```json
{
  "codigo": "A3KR7Z",
  "total": "9.20",
  "hora_recogida": "11:15",
  "metodo_pago": "Bizum",
  "estado": "pendiente"
}
```

---

## 🔗 Conectar el frontend HTML

En `api-cafeteria.html`, reemplaza la función `seleccionarHora` para que llame a la API:

```javascript
const API = 'http://localhost:8000/api';

async function seleccionarHora(hora) {
    cerrarModales();
    const payload = {
        nombre_alumno: '',
        metodo_pago: metodoPago,
        hora_recogida: hora,
        lineas: carrito.map(item => ({
            producto_id: item.id,
            opciones: item.opciones || '',
            precio: item.precio
        }))
    };
    const res = await fetch(`${API}/pedidos/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await res.json();
    // Mostrar data.codigo en el ticket de confirmación
    mostrarTicket(data);
}
```
