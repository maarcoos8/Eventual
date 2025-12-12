// Interfaces para la aplicación Eventual

export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  oauth_provider: string;
  created_at: string;
  last_login: string;
}

export interface Evento {
  id: string;
  nombre: string;
  timestamp: string;
  lugar: string;
  latitud: number;
  longitud: number;
  organizador: string;
  imagen?: string;
  created_at: string;
}

export interface EventoCreate {
  nombre: string;
  timestamp: string;
  lugar: string;
  imagen?: string;
}

export interface EventoUpdate {
  nombre?: string;
  timestamp?: string;
  lugar?: string;
  imagen?: string;
}

export interface SessionLog {
  id: string;
  timestamp: string;
  usuario: string;
  caducidad: string;
  token: string;
}

export interface AuthCallbackParams {
  token?: string;
  error?: string;
}
