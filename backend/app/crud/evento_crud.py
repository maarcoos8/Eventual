from beanie import PydanticObjectId
from typing import List, Optional
from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoUpdate


class EventoCRUD:
    """CRUD operations para Eventos"""
    
    @staticmethod
    async def create(evento_data: EventoCreate) -> Evento:
        """Crear un nuevo evento"""
        evento = Evento(**evento_data.model_dump())
        await evento.insert()
        return evento
    
    @staticmethod
    async def get_by_id(evento_id: PydanticObjectId) -> Optional[Evento]:
        """Obtener un evento por ID"""
        return await Evento.get(evento_id)
    
    @staticmethod
    async def get_all() -> List[Evento]:
        """Obtener todos los eventos"""
        return await Evento.find_all().to_list()
    
    @staticmethod
    async def get_by_organizador(organizador_email: str) -> List[Evento]:
        """Obtener todos los eventos de un organizador"""
        return await Evento.find(Evento.organizador == organizador_email).to_list()
    
    @staticmethod
    async def update(evento_id: PydanticObjectId, evento_data: EventoUpdate) -> Optional[Evento]:
        """Actualizar un evento existente"""
        evento = await Evento.get(evento_id)
        if not evento:
            return None
        
        update_data = evento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(evento, field, value)
        
        await evento.save()
        return evento
    
    @staticmethod
    async def delete(evento_id: PydanticObjectId) -> bool:
        """Eliminar un evento"""
        evento = await Evento.get(evento_id)
        if not evento:
            return False
        await evento.delete()
        return True
    
    @staticmethod
    async def get_by_location_range(
        min_lat: float, 
        max_lat: float, 
        min_lon: float, 
        max_lon: float
    ) -> List[Evento]:
        """Obtener eventos dentro de un rango geográfico"""
        return await Evento.find(
            Evento.latitud >= min_lat,
            Evento.latitud <= max_lat,
            Evento.longitud >= min_lon,
            Evento.longitud <= max_lon
        ).to_list()
