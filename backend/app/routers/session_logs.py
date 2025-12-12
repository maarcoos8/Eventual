from fastapi import APIRouter, Depends
from typing import List
from app.schemas.session_log import SessionLogResponse
from app.crud.session_log_crud import SessionLogCRUD
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/session-logs", tags=["Session Logs"])


@router.get("/", response_model=List[SessionLogResponse])
async def get_session_logs(current_user: User = Depends(get_current_user)):
    """Obtener todos los logs de sesión ordenados por timestamp descendente"""
    logs = await SessionLogCRUD.get_all_ordered()
    return [
        SessionLogResponse(
            id=str(log.id),
            timestamp=log.timestamp,
            usuario=log.usuario,
            caducidad=log.caducidad,
            token=log.token
        )
        for log in logs
    ]
