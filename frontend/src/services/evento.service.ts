// Servicio para gestión de eventos
import type { Evento, EventoCreate, EventoUpdate } from '@/interfaces/eventual';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class EventoService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('auth_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  /**
   * Buscar eventos cercanos a una dirección
   */
  async buscarEventosCercanos(direccion: string): Promise<{ eventos: Evento[]; coordenadas_busqueda: { lat: number; lon: number } }> {
    const response = await fetch(
      `${API_URL}/eventos/buscar?direccion=${encodeURIComponent(direccion)}`
    );
    if (!response.ok) {
      throw new Error('Error al buscar eventos');
    }
    return response.json();
  }

  /**
   * Obtener todos los eventos
   */
  async obtenerTodos(): Promise<Evento[]> {
    const response = await fetch(`${API_URL}/eventos/`);
    if (!response.ok) {
      throw new Error('Error al obtener eventos');
    }
    return response.json();
  }

  /**
   * Obtener un evento por ID
   */
  async obtenerPorId(id: string): Promise<Evento> {
    const response = await fetch(`${API_URL}/eventos/${id}`);
    if (!response.ok) {
      throw new Error('Error al obtener evento');
    }
    return response.json();
  }

  /**
   * Obtener eventos del usuario actual
   */
  async obtenerMisEventos(): Promise<Evento[]> {
    const response = await fetch(`${API_URL}/eventos/mis-eventos`, {
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Error al obtener tus eventos');
    }
    return response.json();
  }

  /**
   * Crear un nuevo evento
   */
  async crear(evento: EventoCreate): Promise<Evento> {
    const response = await fetch(`${API_URL}/eventos/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(evento),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al crear evento');
    }
    return response.json();
  }

  /**
   * Actualizar un evento existente
   */
  async actualizar(id: string, evento: EventoUpdate): Promise<Evento> {
    const response = await fetch(`${API_URL}/eventos/${id}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(evento),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al actualizar evento');
    }
    return response.json();
  }

  /**
   * Eliminar un evento
   */
  async eliminar(id: string): Promise<void> {
    const response = await fetch(`${API_URL}/eventos/${id}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al eliminar evento');
    }
  }

  /**
   * Subir imagen al backend (que la sube a Cloudinary)
   */
  async subirImagen(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_URL}/eventos/upload-image`, {
      method: 'POST',
      headers: {
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al subir imagen');
    }

    const data = await response.json();
    return data.url;
  }
}

export default new EventoService();
