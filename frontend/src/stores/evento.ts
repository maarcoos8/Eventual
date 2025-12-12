// Store para gestión de eventos con Pinia
import { defineStore } from 'pinia';
import type { Evento, EventoCreate, EventoUpdate } from '@/interfaces/eventual';
import eventoService from '@/services/evento.service';

interface EventoState {
  eventos: Evento[];
  eventoActual: Evento | null;
  loading: boolean;
  error: string | null;
  direccionBusqueda: string;
  coordenadasBusqueda: { lat: number; lon: number } | null;
}

export const useEventoStore = defineStore('evento', {
  state: (): EventoState => ({
    eventos: [],
    eventoActual: null,
    loading: false,
    error: null,
    direccionBusqueda: '',
    coordenadasBusqueda: null,
  }),

  actions: {
    async buscarEventosCercanos(direccion: string) {
      this.loading = true;
      this.error = null;
      this.direccionBusqueda = direccion;
      try {
        const resultado = await eventoService.buscarEventosCercanos(direccion);
        this.eventos = resultado.eventos;
        // Usar las coordenadas de la ubicación buscada, no del primer evento
        this.coordenadasBusqueda = {
          lat: resultado.coordenadas_busqueda.lat,
          lon: resultado.coordenadas_busqueda.lon,
        };
      } catch (error: any) {
        this.error = error.message || 'Error al buscar eventos';
        this.eventos = [];
      } finally {
        this.loading = false;
      }
    },

    async obtenerTodos() {
      this.loading = true;
      this.error = null;
      try {
        this.eventos = await eventoService.obtenerTodos();
      } catch (error: any) {
        this.error = error.message || 'Error al obtener eventos';
      } finally {
        this.loading = false;
      }
    },

    async obtenerPorId(id: string) {
      this.loading = true;
      this.error = null;
      try {
        this.eventoActual = await eventoService.obtenerPorId(id);
      } catch (error: any) {
        this.error = error.message || 'Error al obtener evento';
      } finally {
        this.loading = false;
      }
    },

    async obtenerMisEventos() {
      this.loading = true;
      this.error = null;
      try {
        this.eventos = await eventoService.obtenerMisEventos();
      } catch (error: any) {
        this.error = error.message || 'Error al obtener tus eventos';
      } finally {
        this.loading = false;
      }
    },

    async crear(evento: EventoCreate) {
      this.loading = true;
      this.error = null;
      try {
        const nuevoEvento = await eventoService.crear(evento);
        this.eventos.push(nuevoEvento);
        return nuevoEvento;
      } catch (error: any) {
        this.error = error.message || 'Error al crear evento';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async actualizar(id: string, evento: EventoUpdate) {
      this.loading = true;
      this.error = null;
      try {
        const eventoActualizado = await eventoService.actualizar(id, evento);
        const index = this.eventos.findIndex((e) => e.id === id);
        if (index !== -1) {
          this.eventos[index] = eventoActualizado;
        }
        if (this.eventoActual?.id === id) {
          this.eventoActual = eventoActualizado;
        }
        return eventoActualizado;
      } catch (error: any) {
        this.error = error.message || 'Error al actualizar evento';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async eliminar(id: string) {
      this.loading = true;
      this.error = null;
      try {
        await eventoService.eliminar(id);
        this.eventos = this.eventos.filter((e) => e.id !== id);
        if (this.eventoActual?.id === id) {
          this.eventoActual = null;
        }
      } catch (error: any) {
        this.error = error.message || 'Error al eliminar evento';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async subirImagen(file: File): Promise<string> {
      this.loading = true;
      this.error = null;
      try {
        return await eventoService.subirImagen(file);
      } catch (error: any) {
        this.error = error.message || 'Error al subir imagen';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    clearError() {
      this.error = null;
    },
  },
});
