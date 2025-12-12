# Eventual - Frontend Documentation

## Estructura Completa Implementada

### 📁 Estructura de Archivos

```
frontend/
├── src/
│   ├── components/
│   │   ├── EventoCard.vue          # Tarjeta de evento para lista
│   │   └── MapaEventos.vue         # Mapa con Leaflet y marcadores
│   │
│   ├── interfaces/
│   │   └── eventual.ts             # Interfaces TypeScript
│   │
│   ├── services/
│   │   ├── auth.service.ts         # Servicio de autenticación
│   │   ├── evento.service.ts       # Servicio de eventos
│   │   └── session-log.service.ts  # Servicio de logs
│   │
│   ├── stores/
│   │   ├── auth.ts                 # Store de autenticación
│   │   └── evento.ts               # Store de eventos
│   │
│   ├── views/
│   │   ├── Home.vue                # Página principal (búsqueda + mapa)
│   │   ├── DetalleEvento.vue       # Detalles del evento
│   │   ├── FormularioEvento.vue    # Crear/Editar evento
│   │   ├── SessionLogs.vue         # Historial de sesiones
│   │   ├── Login.vue               # (Existente)
│   │   └── AuthCallback.vue        # (Existente)
│   │
│   ├── router/
│   │   └── index.ts                # Configuración de rutas
│   │
│   └── main.ts
│
├── .env.example                    # Variables de entorno
└── package.json
```

### 🎯 Funcionalidades Implementadas

#### 1. **Home.vue** - Página Principal
- Buscador de eventos por dirección
- Lista de eventos cercanos ordenados por fecha
- Mapa con marcadores de eventos
- Botones flotantes:
  - `+` Crear evento (solo autenticado)
  - Lista - Ver logs de sesiones (solo autenticado)
- Login/Logout en el header

#### 2. **MapaEventos.vue** - Componente de Mapa
- Integración con Leaflet
- Marcadores interactivos en cada evento
- Popups con información del evento
- Centrado automático en búsqueda

#### 3. **EventoCard.vue** - Tarjeta de Evento
- Muestra: nombre, organizador, fecha, lugar, imagen
- Click para ver detalles

#### 4. **DetalleEvento.vue** - Vista de Detalles
- Información completa del evento
- Mapa individual del evento
- Botones de editar/eliminar (solo organizador)
- Confirmación antes de eliminar

#### 5. **FormularioEvento.vue** - Crear/Editar
- Formulario para nombre, lugar, fecha/hora
- Upload de imagen a Cloudinary
- Preview de imagen
- Validaciones
- Mismo componente para crear y editar

#### 6. **SessionLogs.vue** - Historial de Sesiones
- Lista de todos los logins
- Información: timestamp, usuario, caducidad, token
- Ordenados por fecha descendente

### 🔧 Configuración Necesaria

#### Variables de Entorno (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_CLOUDINARY_CLOUD_NAME=tu_cloud_name
VITE_CLOUDINARY_UPLOAD_PRESET=tu_upload_preset
```

#### Instalación
```bash
cd frontend
npm install
```

#### Desarrollo
```bash
npm run dev
```

### 📍 Rutas Configuradas

- `/` - Home (búsqueda y lista de eventos)
- `/login` - Login con Google
- `/auth/callback` - Callback OAuth
- `/evento/:id` - Detalles del evento
- `/crear-evento` - Crear nuevo evento (requiere auth)
- `/editar-evento/:id` - Editar evento (requiere auth + ser organizador)
- `/session-logs` - Historial de sesiones (requiere auth)

### 🎨 Características UI/UX

- **Mobile First** con Ionic
- Diseño responsive
- Spinners de carga
- Toasts para mensajes de error/éxito
- Alertas de confirmación para acciones destructivas
- Preview de imágenes antes de subir
- Estados vacíos con iconos y mensajes

### 🔐 Seguridad

- Token JWT almacenado en localStorage
- Headers de autorización automáticos en servicios
- Verificación de organizador en edición/eliminación
- Rutas protegidas con meta `requiresAuth`

### 📦 Servicios

#### EventoService
- `buscarEventosCercanos(direccion)`
- `obtenerTodos()`
- `obtenerPorId(id)`
- `obtenerMisEventos()`
- `crear(evento)`
- `actualizar(id, evento)`
- `eliminar(id)`
- `subirImagen(file)` - Upload a Cloudinary

#### SessionLogService
- `obtenerLogs()` - Historial completo de sesiones

#### AuthService
- `loginWithGoogle()` - Redirige a OAuth
- `setToken(token)` - Guarda token
- `logout()` - Cierra sesión
- `getCurrentUser()` - Obtiene usuario actual
- `isAuthenticated()` - Verifica si hay token

### 🗂️ Stores (Pinia)

#### useEventoStore
- State: `eventos`, `eventoActual`, `loading`, `error`, `direccionBusqueda`, `coordenadasBusqueda`
- Actions: todas las operaciones de eventos

#### useAuthStore
- State: `user`, `loading`, `error`
- Computed: `isAuthenticated`
- Actions: login, logout, loadUser

### ✅ Lista de Verificación

- [x] Interfaces TypeScript
- [x] Servicios de API
- [x] Stores con Pinia
- [x] Componentes reutilizables
- [x] Vistas completas
- [x] Router configurado
- [x] Integración con Leaflet
- [x] Upload a Cloudinary
- [x] Manejo de errores
- [x] Estados de carga
- [x] Autenticación OAuth
- [x] Protección de rutas

### 🚀 Próximos Pasos

1. Crear archivo `.env` con tus credenciales
2. Configurar cuenta de Cloudinary
3. Ejecutar `npm install`
4. Ejecutar `npm run dev`
5. Probar flujo completo:
   - Login con Google
   - Buscar eventos
   - Ver mapa
   - Crear evento
   - Ver logs de sesiones
