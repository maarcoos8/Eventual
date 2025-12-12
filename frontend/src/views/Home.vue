<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Eventual - Eventos Cercanos</ion-title>
        <ion-buttons slot="end">
          <ion-button v-if="!authStore.isAuthenticated" @click="authStore.loginWithGoogle">
            <ion-icon :icon="logIn"></ion-icon>
            Login
          </ion-button>
          <ion-button v-else @click="authStore.logout">
            <ion-icon :icon="logOut"></ion-icon>
            Logout
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div class="container">
        <!-- Buscador -->
        <div class="search-section">
          <ion-searchbar
            v-model="direccion"
            placeholder="Buscar eventos por dirección..."
            @keyup.enter="buscar"
          ></ion-searchbar>
        </div>

        <!-- Botones de acción -->
        <div class="action-buttons" v-if="authStore.isAuthenticated">
          <ion-button @click="verLogs" color="secondary" expand="block">
            <ion-icon :icon="list" slot="start"></ion-icon>
            Historial de Sesiones
          </ion-button>
          <ion-button @click="crearEvento" expand="block">
            <ion-icon :icon="add" slot="start"></ion-icon>
            Crear Evento
          </ion-button>
        </div>

        <!-- Mapa -->
        <div class="map-container" v-if="eventoStore.coordenadasBusqueda">
          <MapaEventos
            :eventos="eventoStore.eventos"
            :centro="eventoStore.coordenadasBusqueda"
          />
        </div>

        <!-- Lista de eventos -->
        <div class="eventos-list">
          <ion-list v-if="eventoStore.eventos.length > 0">
            <ion-list-header>
              <ion-label>Eventos Cercanos ({{ eventoStore.eventos.length }})</ion-label>
            </ion-list-header>
            <EventoCard
              v-for="evento in eventoStore.eventos"
              :key="evento.id"
              :evento="evento"
              @click="verDetalle(evento.id)"
            />
          </ion-list>

          <div v-else-if="!eventoStore.loading" class="empty-state">
            <ion-icon :icon="calendar" size="large"></ion-icon>
            <p>Busca eventos por dirección para comenzar</p>
          </div>

          <div v-if="eventoStore.loading" class="loading">
            <ion-spinner></ion-spinner>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonSearchbar,
  IonList,
  IonListHeader,
  IonLabel,
  IonIcon,
  IonSpinner,
  IonButtons,
  IonButton,
} from '@ionic/vue';
import { add, calendar, logIn, logOut, list } from 'ionicons/icons';
import { useEventoStore } from '@/stores/evento';
import { useAuthStore } from '@/stores/auth';
import MapaEventos from '@/components/MapaEventos.vue';
import EventoCard from '@/components/EventoCard.vue';

const router = useRouter();
const eventoStore = useEventoStore();
const authStore = useAuthStore();
const direccion = ref('');

const buscar = async () => {
  if (direccion.value.trim()) {
    await eventoStore.buscarEventosCercanos(direccion.value);
  }
};

const verDetalle = (id: string) => {
  router.push(`/evento/${id}`);
};

const crearEvento = () => {
  router.push('/crear-evento');
};

const verLogs = () => {
  router.push('/session-logs');
};
</script>

<style scoped>
.container {
  padding: 16px;
}

.search-section {
  margin-bottom: 16px;
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.map-container {
  height: 400px;
  margin-bottom: 24px;
  border-radius: 8px;
  overflow: hidden;
}

.eventos-list {
  margin-bottom: 24px;
}

.empty-state {
  text-align: center;
  padding: 48px 16px;
  color: var(--ion-color-medium);
}

.empty-state ion-icon {
  margin-bottom: 16px;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 32px;
}
</style>
