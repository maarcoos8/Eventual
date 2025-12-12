"""
Entry point para Vercel Serverless Functions
Exporta directamente la app FastAPI para que Vercel la maneje
"""
import sys
from pathlib import Path

# Añadir backend al path para poder importar app
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app

# Exportar la app directamente - Vercel maneja ASGI nativamente
app = app
