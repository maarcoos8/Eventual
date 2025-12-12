// Servicio para gestión de logs de sesión
import type { SessionLog } from '@/interfaces/eventual';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_PREFIX = import.meta.env.PROD ? '/api' : '';

class SessionLogService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('auth_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  /**
   * Obtener todos los logs de sesión
   */
  async obtenerLogs(): Promise<SessionLog[]> {
    const response = await fetch(`${API_URL}${API_PREFIX}/session-logs/`, {
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Error al obtener logs de sesión');
    }
    return response.json();
  }
}

export default new SessionLogService();
