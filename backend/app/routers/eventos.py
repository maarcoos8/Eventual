from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from beanie import PydanticObjectId
from typing import List
from app.schemas.evento import EventoCreate, EventoUpdate, EventoResponse, EventosBusquedaResponse
from app.crud.evento_crud import EventoCRUD
from app.core.auth import get_current_user
from app.core.geocoding import geocode_location
from app.core.cloudinary_service import upload_image
from app.models.user import User

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.get("/buscar", response_model=EventosBusquedaResponse)
async def buscar_eventos_cercanos(direccion: str = Query(..., description="Dirección para buscar eventos cercanos")):
    """Buscar eventos cercanos a una dirección (distancia < 0.2 en lat/lon)"""
    # Obtener coordenadas de la dirección
    coords = await geocode_location(direccion)
    if not coords:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudieron obtener coordenadas para: {direccion}"
        )
    
    lat, lon = coords
    # Buscar eventos en rango de 0.2 grados (~22km)
    eventos = await EventoCRUD.get_by_location_range(
        min_lat=lat - 0.2,
        max_lat=lat + 0.2,
        min_lon=lon - 0.2,
        max_lon=lon + 0.2
    )
    
    # Ordenar por timestamp
    eventos_ordenados = sorted(eventos, key=lambda e: e.timestamp)
    
    eventos_response = [
        EventoResponse(
            id=str(evento.id),
            nombre=evento.nombre,
            timestamp=evento.timestamp,
            lugar=evento.lugar,
            latitud=evento.latitud,
            longitud=evento.longitud,
            organizador=evento.organizador,
            imagen=evento.imagen,
            created_at=evento.created_at
        )
        for evento in eventos_ordenados
    ]
    
    return EventosBusquedaResponse(
        eventos=eventos_response,
        coordenadas_busqueda={"lat": lat, "lon": lon}
    )


@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
async def create_evento(
    evento_data: EventoCreate,
    current_user: User = Depends(get_current_user)
):
    """Crear un nuevo evento (requiere autenticación)"""
    # Obtener coordenadas por geocoding
    coords = await geocode_location(evento_data.lugar)
    if not coords:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudieron obtener coordenadas para la dirección: {evento_data.lugar}"
        )
    
    # Importar el modelo Evento para crear la instancia directamente
    from app.models.evento import Evento
    
    # Crear el evento con todos los datos
    evento = Evento(
        nombre=evento_data.nombre,
        timestamp=evento_data.timestamp,
        lugar=evento_data.lugar,
        latitud=coords[0],
        longitud=coords[1],
        organizador=current_user.email,
        imagen=evento_data.imagen
    )
    await evento.insert()
    return EventoResponse(
        id=str(evento.id),
        nombre=evento.nombre,
        timestamp=evento.timestamp,
        lugar=evento.lugar,
        latitud=evento.latitud,
        longitud=evento.longitud,
        organizador=evento.organizador,
        imagen=evento.imagen,
        created_at=evento.created_at
    )


@router.get("/", response_model=List[EventoResponse])
async def get_all_eventos():
    """Obtener todos los eventos"""
    eventos = await EventoCRUD.get_all()
    return [
        EventoResponse(
            id=str(evento.id),
            nombre=evento.nombre,
            timestamp=evento.timestamp,
            lugar=evento.lugar,
            latitud=evento.latitud,
            longitud=evento.longitud,
            organizador=evento.organizador,
            imagen=evento.imagen,
            created_at=evento.created_at
        )
        for evento in eventos
    ]


@router.get("/mis-eventos", response_model=List[EventoResponse])
async def get_my_eventos(current_user: User = Depends(get_current_user)):
    """Obtener eventos creados por el usuario actual"""
    eventos = await EventoCRUD.get_by_organizador(current_user.email)
    return [
        EventoResponse(
            id=str(evento.id),
            nombre=evento.nombre,
            timestamp=evento.timestamp,
            lugar=evento.lugar,
            latitud=evento.latitud,
            longitud=evento.longitud,
            organizador=evento.organizador,
            imagen=evento.imagen,
            created_at=evento.created_at
        )
        for evento in eventos
    ]


@router.get("/{evento_id}", response_model=EventoResponse)
async def get_evento(evento_id: str):
    """Obtener un evento por ID"""
    try:
        evento = await EventoCRUD.get_by_id(PydanticObjectId(evento_id))
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        return EventoResponse(
            id=str(evento.id),
            nombre=evento.nombre,
            timestamp=evento.timestamp,
            lugar=evento.lugar,
            latitud=evento.latitud,
            longitud=evento.longitud,
            organizador=evento.organizador,
            imagen=evento.imagen,
            created_at=evento.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID inválido: {str(e)}"
        )


@router.put("/{evento_id}", response_model=EventoResponse)
async def update_evento(
    evento_id: str,
    evento_data: EventoUpdate,
    current_user: User = Depends(get_current_user)
):
    """Actualizar un evento (solo el organizador)"""
    try:
        evento = await EventoCRUD.get_by_id(PydanticObjectId(evento_id))
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        # Verificar que el usuario actual es el organizador
        if evento.organizador != current_user.email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para actualizar este evento"
            )
        
        # Actualizar campos del evento
        update_data = evento_data.model_dump(exclude_unset=True)
        
        # Si se actualiza el lugar, obtener nuevas coordenadas
        if "lugar" in update_data and update_data["lugar"]:
            coords = await geocode_location(update_data["lugar"])
            if coords:
                update_data["latitud"] = coords[0]
                update_data["longitud"] = coords[1]
        
        # Aplicar actualizaciones
        for field, value in update_data.items():
            setattr(evento, field, value)
        
        await evento.save()
        updated_evento = evento
        return EventoResponse(
            id=str(updated_evento.id),
            nombre=updated_evento.nombre,
            timestamp=updated_evento.timestamp,
            lugar=updated_evento.lugar,
            latitud=updated_evento.latitud,
            longitud=updated_evento.longitud,
            organizador=updated_evento.organizador,
            imagen=updated_evento.imagen,
            created_at=updated_evento.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar evento: {str(e)}"
        )


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_evento(
    evento_id: str,
    current_user: User = Depends(get_current_user)
):
    """Eliminar un evento (solo el organizador)"""
    try:
        evento = await EventoCRUD.get_by_id(PydanticObjectId(evento_id))
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        # Verificar que el usuario actual es el organizador
        if evento.organizador != current_user.email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este evento"
            )
        
        await EventoCRUD.delete(PydanticObjectId(evento_id))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar evento: {str(e)}"
        )


@router.post("/upload-image", response_model=dict)
async def upload_evento_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Subir una imagen a Cloudinary (requiere autenticación)
    
    Returns:
        {"url": "https://res.cloudinary.com/..."}
    """
    # Validar tipo de archivo
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser una imagen"
        )
    
    # Validar tamaño (max 10MB)
    file_content = await file.read()
    if len(file_content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen no puede superar los 10MB"
        )
    
    try:
        url = await upload_image(file_content, file.filename or "evento.jpg")
        return {"url": url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir imagen: {str(e)}"
        )
