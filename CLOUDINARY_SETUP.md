# Configuración de Cloudinary para Eventual

## ¿Qué es Cloudinary?
Cloudinary es un servicio de almacenamiento y optimización de imágenes en la nube. Lo usamos para almacenar las imágenes de los eventos.

## Pasos para configurar

### 1. Crear cuenta en Cloudinary
1. Ve a https://cloudinary.com
2. Click en "Sign Up" (Registrarse)
3. Crea una cuenta gratuita (no necesitas tarjeta de crédito)

### 2. Obtener Cloud Name
1. Una vez dentro, ve al **Dashboard**
2. En la parte superior verás tu **Cloud Name**
3. Cópialo (ejemplo: `dmxyz123abc`)

### 3. Crear Upload Preset
1. Ve a **Settings** (⚙️ en la esquina superior derecha)
2. Click en la pestaña **Upload**
3. Scroll hasta **Upload presets**
4. Click en **Add upload preset**
5. Configura:
   - **Upload preset name**: `eventual_uploads` (o el nombre que prefieras)
   - **Signing Mode**: Selecciona **Unsigned** (muy importante!)
   - **Folder**: `eventos` (opcional, para organizar las imágenes)
6. Click en **Save**

### 4. Configurar el Frontend
Edita el archivo `frontend/.env` y reemplaza:

```env
VITE_CLOUDINARY_CLOUD_NAME=tu_cloud_name_aqui
VITE_CLOUDINARY_UPLOAD_PRESET=eventual_uploads
```

Ejemplo:
```env
VITE_CLOUDINARY_CLOUD_NAME=dmxyz123abc
VITE_CLOUDINARY_UPLOAD_PRESET=eventual_uploads
```

### 5. Reiniciar Docker
Después de configurar el `.env`, reinicia los contenedores:

```bash
docker-compose down
docker-compose up --build
```

## Verificar que funciona

1. Accede a la aplicación en `http://localhost:5173`
2. Inicia sesión con Google
3. Click en el botón `+` para crear un evento
4. Sube una imagen
5. Si todo está bien configurado, verás la preview de la imagen
6. Al guardar, la imagen se subirá a Cloudinary y el evento se creará con la URL de la imagen

## Límites del plan gratuito
- 25 GB de almacenamiento
- 25 GB de ancho de banda mensual
- Transformaciones de imágenes básicas
- Suficiente para desarrollo y proyectos pequeños

## Solución de problemas

### Error: "Cannot find module VITE_CLOUDINARY_CLOUD_NAME"
- Asegúrate de que el archivo `.env` existe en `frontend/`
- Verifica que las variables empiezan con `VITE_`
- Reinicia el contenedor de frontend

### Error al subir imagen
- Verifica que el **Upload preset** esté en modo **Unsigned**
- Comprueba que el nombre del preset coincide exactamente
- Revisa la consola del navegador para ver el error específico
