# API Eventual - Documentación

## Descripción
API para gestión de eventos con geolocalización, OAuth 2.0 con Google, geocoding automático y almacenamiento de imágenes en Cloudinary.

## Tecnologías
- **Framework**: FastAPI
- **Base de Datos**: MongoDB con Beanie ODM
- **Autenticación**: OAuth 2.0 (Google) + JWT
- **Geocoding**: OpenStreetMap Nominatim
- **Imágenes**: Cloudinary

---

## Endpoints Principales

### 🔐 Autenticación (`/auth`)

#### Login con Google
```http
GET /auth/login/google
```
Inicia el flujo OAuth con Google.

#### Callback OAuth
```http
GET /auth/callback/google
```
Procesa la respuesta de Google y registra la sesión.

#### Obtener Usuario Actual
```http
GET /auth/me
```
Requiere: Token JWT
Retorna información del usuario autenticado.

#### Logout
```http
POST /auth/logout
```

---

### 📅 Eventos (`/eventos`)

#### Buscar Eventos Cercanos
```http
GET /eventos/buscar?direccion={direccion}
```
- **Público** (no requiere autenticación)
- Busca eventos dentro de 0.2 grados (~22km) de la dirección
- Ordenados por timestamp
- Retorna: lista de eventos con coordenadas para mostrar en mapa

**Ejemplo:**
```
GET /eventos/buscar?direccion=Madrid, España
```

#### Listar Todos los Eventos
```http
GET /eventos/
```
- **Público**
- Retorna todos los eventos

#### Obtener Evento por ID
```http
GET /eventos/{evento_id}
```
- **Público**
- Retorna detalles completos del evento

#### Obtener Mis Eventos
```http
GET /eventos/mis-eventos
```
- **Requiere autenticación**
- Retorna eventos creados por el usuario actual

#### Crear Evento
```http
POST /eventos/
```
- **Requiere autenticación** (token JWT)
- Las coordenadas se obtienen automáticamente por geocoding
- El organizador se asigna automáticamente al usuario autenticado

**Body:**
```json
{
  "nombre": "Concierto de Rock",
  "timestamp": "2025-12-20T20:00:00",
  "lugar": "Av. Corrientes 1234, Buenos Aires",
  "imagen": "https://res.cloudinary.com/..."
}
```

#### Actualizar Evento
```http
PUT /eventos/{evento_id}
```
- **Requiere autenticación**
- Solo el organizador puede actualizar
- Si se cambia el lugar, se recalculan las coordenadas

**Body:**
```json
{
  "nombre": "Nuevo nombre",
  "timestamp": "2025-12-21T20:00:00",
  "lugar": "Nueva dirección",
  "imagen": "https://res.cloudinary.com/..."
}
```

#### Eliminar Evento
```http
DELETE /eventos/{evento_id}
```
- **Requiere autenticación**
- Solo el organizador puede eliminar

---

### 📊 Logs de Sesión (`/session-logs`)

#### Ver Todos los Logs
```http
GET /session-logs/
```
- **Requiere autenticación**
- Retorna todos los registros de login ordenados por timestamp descendente
- Información incluida:
  - Timestamp del login
  - Email del usuario
  - Timestamp de caducidad del token
  - Token JWT completo

---

## Modelos de Datos

### Evento
```javascript
{
  "id": "string",
  "nombre": "string",          // Título del evento
  "timestamp": "datetime",     // Fecha/hora del evento
  "lugar": "string",           // Dirección postal
  "latitud": "float",          // Coordenada GPS (automática)
  "longitud": "float",         // Coordenada GPS (automática)
  "organizador": "email",      // Email del creador
  "imagen": "string",          // URL de Cloudinary
  "created_at": "datetime"     // Fecha de creación
}
```

### SessionLog
```javascript
{
  "id": "string",
  "timestamp": "datetime",     // Momento del login
  "usuario": "email",          // Email del usuario
  "caducidad": "datetime",     // Expiración del token (7 días)
  "token": "string"            // Token JWT completo
}
```

### User
```javascript
{
  "email": "email",
  "name": "string",
  "picture": "string",         // URL de foto de perfil
  "oauth_provider": "google",
  "oauth_id": "string",
  "last_login": "datetime"
}
```

---

## Flujo de Trabajo

### 1. Login
1. Usuario hace clic en "Login con Google"
2. Se redirige a `/auth/login/google`
3. Google autentica al usuario
4. Callback en `/auth/callback/google`
5. Se crea/actualiza el usuario en BD
6. Se genera token JWT (válido 7 días)
7. **Se registra la sesión en SessionLog**
8. Se redirige al frontend con el token

### 2. Búsqueda de Eventos
1. Usuario ingresa una dirección en el buscador
2. Frontend llama a `GET /eventos/buscar?direccion={direccion}`
3. Backend obtiene coordenadas vía geocoding
4. Busca eventos en rango de ±0.2 grados
5. Retorna lista ordenada por timestamp
6. Frontend muestra:
   - Lista de eventos (nombre, organizador, botón detalles)
   - Mapa con marcadores de eventos cercanos

### 3. Crear Evento
1. Usuario autenticado llena formulario (nombre, lugar, fecha/hora)
2. Usuario sube imagen a Cloudinary (desde frontend)
3. Frontend envía `POST /eventos/` con token JWT
4. Backend:
   - Valida token
   - Obtiene coordenadas por geocoding del lugar
   - Asigna organizador automáticamente
   - Guarda evento en BD
5. Retorna evento creado

### 4. Modificar/Borrar Evento
1. Usuario autenticado accede a sus eventos
2. Backend verifica que sea el organizador
3. Si cambia lugar: recalcula coordenadas
4. Actualiza/elimina según acción

---

## Seguridad

### Rutas Públicas (sin autenticación)
- `GET /eventos/buscar`
- `GET /eventos/`
- `GET /eventos/{evento_id}`

### Rutas Protegidas (requieren JWT)
- `POST /eventos/` - Crear evento
- `PUT /eventos/{evento_id}` - Solo organizador
- `DELETE /eventos/{evento_id}` - Solo organizador
- `GET /eventos/mis-eventos`
- `GET /session-logs/`

### Validaciones
- Token JWT válido (7 días)
- Verificación de organizador en update/delete
- Geocoding automático (no se confía en coordenadas del cliente)

---

## Variables de Entorno Requeridas

```env
# MongoDB
MONGODB_CONNECTION_STRING=mongodb://...
MONGODB_DATABASE_NAME=eventual

# OAuth Google
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# JWT
JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256

# Frontend
FRONTEND_URL=http://localhost:5173
```

---

## Notas Importantes

1. **Geocoding Automático**: Las coordenadas NUNCA se envían desde el frontend. Siempre se calculan en el backend a partir de la dirección.

2. **Log Permanente**: Cada login queda registrado permanentemente en `session_logs` con timestamp, usuario, caducidad y token.

3. **Búsqueda por Proximidad**: El rango de 0.2 grados equivale aproximadamente a 22km. Puede ajustarse según necesidades.

4. **Imágenes**: El upload a Cloudinary se hace desde el frontend. El backend solo recibe y almacena la URL generada.

5. **Mapa**: El frontend debe implementar el mapa (usando Leaflet u otro). El backend provee las coordenadas de los eventos.
