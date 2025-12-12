from typing import List
from app.models.session_log import SessionLog
from app.schemas.session_log import SessionLogCreate


class SessionLogCRUD:
    """CRUD operations para SessionLog"""
    
    @staticmethod
    async def create(log_data: SessionLogCreate) -> SessionLog:
        """Crear un nuevo registro de sesión"""
        log = SessionLog(**log_data.model_dump())
        await log.insert()
        return log
    
    @staticmethod
    async def get_all_ordered() -> List[SessionLog]:
        """Obtener todos los logs ordenados por timestamp descendente"""
        return await SessionLog.find_all().sort(-SessionLog.timestamp).to_list()
