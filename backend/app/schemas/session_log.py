from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class SessionLogCreate(BaseModel):
    """Schema para crear un registro de sesión"""
    usuario: EmailStr
    caducidad: datetime
    token: str


class SessionLogResponse(BaseModel):
    """Schema para la respuesta de un registro de sesión"""
    id: str
    timestamp: datetime
    usuario: str
    caducidad: datetime
    token: str
