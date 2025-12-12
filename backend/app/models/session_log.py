from beanie import Document, PydanticObjectId
from pydantic import EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class SessionLog(Document):
    """
    Modelo de registro de sesiones de usuario
    Almacena información de cada login realizado
    """
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # Momento del login
    usuario: EmailStr = Field(..., index=True)  # Email del usuario
    caducidad: datetime  # Timestamp de expiración del token
    token: str  # Token de identificación JWT
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PydanticObjectId: str},
        json_schema_extra={
            "example": {
                "timestamp": "2025-12-12T10:30:00",
                "usuario": "user@example.com",
                "caducidad": "2025-12-19T10:30:00",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )
    
    class Settings:
        name = "session_logs"
