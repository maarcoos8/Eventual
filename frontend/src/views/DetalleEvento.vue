<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>Detalles del Evento</ion-title>
        <ion-buttons slot="end" v-if="esOrganizador">
          <ion-button @click="editar">
            <ion-icon :icon="create"></ion-icon>
          </ion-button>
          <ion-button @click="confirmarEliminar" color="danger">
            <ion-icon :icon="trash"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div v-if="eventoStore.loading" class="loading">
        <ion-spinner></ion-spinner>
      </div>

      <div v-else-if="eventoStore.eventoActual" class="evento-detalle">
        <ion-card>
          <ion-card-header>
            <ion-card-title>{{ eventoStore.eventoActual.nombre }}</ion-card-title>
          </ion-card-header>

          <ion-card-content>
            <div class="content-layout">
              <ion-list class="info-list">
                <ion-item>
                  <ion-icon :icon="calendar" slot="start"></ion-icon>
                  <ion-label>
                    <h3>Fecha y Hora</h3>
                    <p>{{ formatFecha(eventoStore.eventoActual.timestamp) }}</p>
                  </ion-label>
                </ion-item>

                <ion-item>
                  <ion-icon :icon="location" slot="start"></ion-icon>
                  <ion-label>
                    <h3>Lugar</h3>
                    <p>{{ eventoStore.eventoActual.lugar }}</p>
                  </ion-label>
                </ion-item>

                <ion-item>
                  <ion-icon :icon="person" slot="start"></ion-icon>
                  <ion-label>
                    <h3>Organizador</h3>
                    <p>{{ eventoStore.eventoActual.organizador }}</p>
                  </ion-label>
                </ion-item>

                <ion-item>
                  <ion-icon :icon="navigate" slot="start"></ion-icon>
                  <ion-label>
                    <h3>Coordenadas</h3>
                    <p>{{ eventoStore.eventoActual.latitud }}, {{ eventoStore.eventoActual.longitud }}</p>
                  </ion-label>
                </ion-item>
              </ion-list>
              
              <img v-if="eventoStore.eventoActual.imagen" :src="eventoStore.eventoActual.imagen" class="evento-imagen" />
            </div>
          </ion-card-content>
        </ion-card>

        <!-- Mapa del evento -->
        <div class="map-container">
          <MapaEventos
            :eventos="[eventoStore.eventoActual]"
            :centro="{ lat: eventoStore.eventoActual.latitud, lon: eventoStore.eventoActual.longitud }"
          />
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonBackButton,
  IonButton,
  IonIcon,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonSpinner,
  alertController,
} from '@ionic/vue';
import { calendar, location, person, navigate, create, trash } from 'ionicons/icons';
import { useEventoStore } from '@/stores/evento';
import { useAuthStore } from '@/stores/auth';
import MapaEventos from '@/components/MapaEventos.vue';

const route = useRoute();
const router = useRouter();
const eventoStore = useEventoStore();
const authStore = useAuthStore();

const esOrganizador = computed(() => {
  return eventoStore.eventoActual?.organizador === authStore.user?.email;
});

onMounted(async () => {
  const id = route.params.id as string;
  await eventoStore.obtenerPorId(id);
});

const formatFecha = (fecha: string) => {
  return new Date(fecha).toLocaleString('es-ES', {
    weekday: 'long',
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const editar = () => {
  router.push(`/editar-evento/${route.params.id}`);
};

const confirmarEliminar = async () => {
  const alert = await alertController.create({
    header: 'Confirmar eliminación',
    message: '¿Estás seguro de que quieres eliminar este evento?',
    buttons: [
      {
        text: 'Cancelar',
        role: 'cancel',
      },
      {
        text: 'Eliminar',
        role: 'destructive',
        handler: async () => {
          await eliminar();
        },
      },
    ],
  });

  await alert.present();
};

const eliminar = async () => {
  try {
    await eventoStore.eliminar(route.params.id as string);
    router.push('/');
  } catch (error) {
    console.error('Error al eliminar evento:', error);
  }
};
</script>

<style scoped>
.loading {
  display: flex;
  justify-content: center;
  padding: 48px;
}

.evento-detalle {
  padding: 16px;
}

.content-layout {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.info-list {
  flex: 1;
  min-width: 0;
}

.evento-imagen {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .content-layout {
    flex-direction: column;
  }
  
  .evento-imagen {
    width: 100%;
    max-width: 250px;
    margin: 0 auto;
  }
}

.map-container {
  height: 300px;
  margin-top: 16px;
  border-radius: 8px;
  overflow: hidden;
}
</style>
