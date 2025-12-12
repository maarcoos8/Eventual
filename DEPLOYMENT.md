# Guía de Despliegue - Eventual

## 🐳 Docker - Desarrollo

### Iniciar todos los servicios
```bash
docker-compose up -d
```

### Ver logs
```bash
docker-compose logs -f
```

### Detener servicios
```bash
docker-compose down
```

## 🚀 Docker - Producción

### 1. Preparar archivos de entorno

**Backend:**
```bash
cp backend/.env.production.example backend/.env.production
# Editar backend/.env.production con valores reales
```

**Frontend:**
```bash
# Crear frontend/.env.production
VITE_API_URL=https://api.tu-dominio.com
VITE_CLOUDINARY_CLOUD_NAME=tu_cloud_name
VITE_CLOUDINARY_UPLOAD_PRESET=tu_upload_preset
```

### 2. Construir y desplegar
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### 3. Verificar estado
```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f
```

## ☁️ Despliegue en la Nube

### Opción 1: Vercel (Backend)

1. **Preparar para serverless:**
   - El archivo `api/index.py` ya está configurado para Vercel
   - El `vercel.json` está en la raíz del proyecto

2. **Desplegar:**
```bash
cd backend
vercel --prod
```

3. **Configurar variables de entorno en Vercel:**
   - `MONGODB_CONNECTION_STRING`
   - `MONGODB_DATABASE_NAME`
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `JWT_SECRET_KEY`
   - `FRONTEND_URL`

### Opción 2: Railway / Render

**Backend:**
1. Conectar repositorio
2. Configurar:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Agregar variables de entorno

**Frontend:**
1. Build Command: `cd frontend && npm install && npm run build`
2. Start Command: Usar servidor estático o Nginx
3. Configurar `VITE_API_URL` apuntando al backend

### Opción 3: AWS / Google Cloud / Azure

**Usar Docker:**
```bash
# Subir imágenes a registry
docker tag eventual-backend:latest registry.example.com/eventual-backend:latest
docker push registry.example.com/eventual-backend:latest

docker tag eventual-frontend:latest registry.example.com/eventual-frontend:latest
docker push registry.example.com/eventual-frontend:latest
```

## 🔐 Seguridad - Checklist Producción

- [ ] Cambiar `JWT_SECRET_KEY` a valor aleatorio seguro
- [ ] Configurar CORS con dominios específicos
- [ ] Usar HTTPS en producción
- [ ] Configurar MongoDB con autenticación
- [ ] Usar variables de entorno (nunca hardcodear secretos)
- [ ] Limitar rate limiting en endpoints públicos
- [ ] Configurar logs apropiados
- [ ] Habilitar health checks
- [ ] Configurar backups de base de datos

## 📊 Monitoreo

### Health Checks

**Backend:**
```bash
curl http://localhost:8000/
```

**Frontend:**
```bash
curl http://localhost/
```

### Logs en Docker
```bash
# Backend
docker logs eventual-backend-prod -f

# Frontend
docker logs eventual-frontend-prod -f
```

## 🔄 Actualizar en Producción

```bash
# 1. Hacer pull de los cambios
git pull origin main

# 2. Reconstruir y reiniciar
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Verificar
docker-compose -f docker-compose.prod.yml ps
```

## 🛠️ Troubleshooting

### Backend no se conecta a MongoDB
- Verificar `MONGODB_CONNECTION_STRING`
- Verificar firewall/whitelist IP en MongoDB Atlas

### Frontend no se conecta al Backend
- Verificar `VITE_API_URL` en `.env.production`
- Verificar CORS en backend
- Verificar network en docker-compose

### OAuth no funciona
- Verificar URLs de redirección en Google Console
- Deben coincidir con `FRONTEND_URL/auth/callback`

## 📝 Comandos Útiles

```bash
# Limpiar todo Docker
docker-compose down -v
docker system prune -a

# Reconstruir solo un servicio
docker-compose up -d --build backend

# Acceder a shell del contenedor
docker exec -it eventual-backend-prod bash

# Ver uso de recursos
docker stats
```
