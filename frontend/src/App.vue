<template>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { useAuthStore } from '@/stores/auth';
import ThemeService from '@/services/shared/theme.service';

const authStore = useAuthStore();

// Inicializar tema y cargar usuario al iniciar la aplicación
onMounted(async () => {
  // FORZAR tema claro siempre (eliminar cualquier configuración anterior)
  localStorage.removeItem('selected-theme');
  ThemeService.setTheme('light');
  console.log('Tema forzado a claro');
  
  await authStore.loadUser();
});
</script>
