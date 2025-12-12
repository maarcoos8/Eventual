import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: 'Eventual - Eventos Cercanos'
    }
  },
  {
    path: '/auth/callback',
    name: 'AuthCallback',
    component: () => import('@/views/AuthCallback.vue'),
    meta: {
      title: 'Autenticando...'
    }
  },
  {
    path: '/evento/:id',
    name: 'DetalleEvento',
    component: () => import('@/views/DetalleEvento.vue'),
    meta: {
      title: 'Detalle del Evento - Eventual'
    }
  },
  {
    path: '/crear-evento',
    name: 'CrearEvento',
    component: () => import('@/views/FormularioEvento.vue'),
    meta: {
      title: 'Crear Evento - Eventual',
      requiresAuth: true
    }
  },
  {
    path: '/editar-evento/:id',
    name: 'EditarEvento',
    component: () => import('@/views/FormularioEvento.vue'),
    meta: {
      title: 'Editar Evento - Eventual',
      requiresAuth: true
    }
  },
  {
    path: '/session-logs',
    name: 'SessionLogs',
    component: () => import('@/views/SessionLogs.vue'),
    meta: {
      title: 'Historial de Sesiones - Eventual',
      requiresAuth: true
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// Navigation guard para rutas protegidas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token');
  
  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth && !token) {
    // Si requiere autenticación y no hay token, redirigir a home
    next('/');
  } else {
    next();
  }
});

export default router;