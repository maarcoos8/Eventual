from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EventoCreate(BaseModel):
    """Schema para crear un nuevo evento"""
    nombre: str = Field(..., min_length=1, max_length=200, description="Nombre o título del evento")
    timestamp: datetime = Field(..., description="Fecha y hora del evento")
    lugar: str = Field(..., max_length=300, description="Dirección postal del evento")
    organizador: Optional[EmailStr] = Field(None, description="Email del organizador (se asigna automáticamente)")
    imagen: Optional[str] = Field(None, description="URL de la imagen en Cloudinary")


class EventoUpdate(BaseModel):
    """Schema para actualizar un evento existente"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=200, description="Nombre o título del evento")
    timestamp: Optional[datetime] = Field(None, description="Fecha y hora del evento")
    lugar: Optional[str] = Field(None, max_length=300, description="Dirección postal del evento")
    imagen: Optional[str] = Field(None, description="URL de la imagen en Cloudinary")


class EventoResponse(BaseModel):
    """Schema para la respuesta de un evento"""
    id: str
    nombre: str
    timestamp: datetime
    lugar: str
    latitud: float
    longitud: float
    organizador: str
    imagen: Optional[str] = None
    created_at: datetime


class EventosBusquedaResponse(BaseModel):
    """Schema para la respuesta de búsqueda de eventos con coordenadas"""
    eventos: list[EventoResponse]
    coordenadas_busqueda: dict[str, float] = Field(..., description="Coordenadas de la ubicación buscada")
