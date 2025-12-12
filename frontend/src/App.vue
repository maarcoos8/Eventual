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

ThemeService.initializeTheme();

const authStore = useAuthStore();

// Cargar usuario al iniciar la aplicación si hay token
onMounted(async () => {
  await authStore.loadUser();
});
</script>
