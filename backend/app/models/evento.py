from beanie import Document, PydanticObjectId
from pydantic import EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class Evento(Document):
    """
    Modelo de Evento
    Almacena eventos con ubicación, fecha/hora, organizador e imagen
    """
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    nombre: str = Field(..., min_length=1, max_length=200)  # Nombre o título del evento
    timestamp: datetime  # Fecha y hora del evento
    lugar: str = Field(..., max_length=300)  # Dirección postal del evento
    latitud: float  # Coordenada GPS latitud
    longitud: float  # Coordenada GPS longitud
    organizador: EmailStr = Field(..., index=True)  # Email del usuario que creó el evento
    imagen: Optional[str] = None  # URL de la imagen en Cloudinary
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PydanticObjectId: str},
        json_schema_extra={
            "example": {
                "nombre": "Concierto de Rock",
                "timestamp": "2025-12-20T20:00:00",
                "lugar": "Av. Corrientes 1234, Buenos Aires",
                "latitud": -34.6037,
                "longitud": -58.3816,
                "organizador": "organizador@example.com",
                "imagen": "https://res.cloudinary.com/demo/image/upload/concierto.jpg"
            }
        }
    )
    
    class Settings:
        name = "eventos"
