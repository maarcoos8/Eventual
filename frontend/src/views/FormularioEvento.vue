<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-back-button default-href="/"></ion-back-button>
        </ion-buttons>
        <ion-title>{{ esEdicion ? 'Editar Evento' : 'Crear Evento' }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <div class="form-container">
        <ion-list>
          <ion-item>
            <ion-input
              v-model="formData.nombre"
              label="Nombre del Evento"
              label-placement="stacked"
              placeholder="Ej: Concierto de Rock"
              counter
              :maxlength="200"
              required
            ></ion-input>
          </ion-item>

          <ion-item>
            <ion-input
              v-model="formData.lugar"
              label="Dirección"
              label-placement="stacked"
              placeholder="Ej: Av. Corrientes 1234, Buenos Aires"
              counter
              :maxlength="300"
              required
            ></ion-input>
          </ion-item>

          <ion-item>
            <ion-input
              v-model="formData.timestamp"
              label="Fecha y Hora"
              label-placement="stacked"
              type="datetime-local"
              required
            ></ion-input>
          </ion-item>

          <ion-item>
            <ion-label position="stacked">Imagen del Evento</ion-label>
            <input
              v-if="!imagenPreview"
              type="file"
              accept="image/*"
              @change="seleccionarImagen"
              ref="fileInput"
            />
          </ion-item>

          <ion-item v-if="imagenPreview" lines="none">
            <div class="imagen-container">
              <img :src="imagenPreview" class="imagen-preview" />
              <div class="imagen-overlay" @click="eliminarImagen">
                <ion-icon :icon="close" class="close-icon"></ion-icon>
              </div>
            </div>
          </ion-item>
        </ion-list>

        <div class="button-container">
          <ion-button expand="block" @click="guardar" :disabled="eventoStore.loading">
            <ion-spinner v-if="eventoStore.loading" slot="start"></ion-spinner>
            {{ esEdicion ? 'Actualizar' : 'Crear Evento' }}
          </ion-button>
        </div>

        <ion-toast
          :is-open="!!mensajeError"
          :message="mensajeError"
          :duration="3000"
          color="danger"
          @didDismiss="mensajeError = ''"
        ></ion-toast>

        <ion-toast
          :is-open="mostrarExito"
          message="Evento guardado correctamente"
          :duration="2000"
          color="success"
          @didDismiss="volverAtras"
        ></ion-toast>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonBackButton,
  IonList,
  IonItem,
  IonInput,
  IonLabel,
  IonButton,
  IonSpinner,
  IonToast,
  IonIcon,
} from '@ionic/vue';
import { close } from 'ionicons/icons';
import { useEventoStore } from '@/stores/evento';
import type { EventoCreate, EventoUpdate } from '@/interfaces/eventual';

const route = useRoute();
const router = useRouter();
const eventoStore = useEventoStore();

const esEdicion = ref(false);
const formData = ref<EventoCreate>({
  nombre: '',
  timestamp: '',
  lugar: '',
  imagen: undefined,
});
const imagenPreview = ref('');
const archivoImagen = ref<File | null>(null);
const mensajeError = ref('');
const mostrarExito = ref(false);

onMounted(async () => {
  const id = route.params.id as string;
  if (id) {
    esEdicion.value = true;
    await eventoStore.obtenerPorId(id);
    if (eventoStore.eventoActual) {
      formData.value = {
        nombre: eventoStore.eventoActual.nombre,
        timestamp: eventoStore.eventoActual.timestamp,
        lugar: eventoStore.eventoActual.lugar,
        imagen: eventoStore.eventoActual.imagen,
      };
      if (eventoStore.eventoActual.imagen) {
        imagenPreview.value = eventoStore.eventoActual.imagen;
      }
    }
  }
});

const seleccionarImagen = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    archivoImagen.value = target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      imagenPreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(target.files[0]);
  }
};

const eliminarImagen = () => {
  imagenPreview.value = '';
  archivoImagen.value = null;
  formData.value.imagen = '';  // Enviar string vacío para actualizar que no hay imagen
};

const guardar = async () => {
  // Validaciones
  if (!formData.value.nombre || !formData.value.lugar || !formData.value.timestamp) {
    mensajeError.value = 'Por favor completa todos los campos obligatorios';
    return;
  }

  try {
    // Subir imagen si hay una nueva
    if (archivoImagen.value) {
      const urlImagen = await eventoStore.subirImagen(archivoImagen.value);
      formData.value.imagen = urlImagen;
    }

    if (esEdicion.value) {
      const updateData: EventoUpdate = {
        nombre: formData.value.nombre,
        timestamp: formData.value.timestamp,
        lugar: formData.value.lugar,
        imagen: formData.value.imagen,
      };
      await eventoStore.actualizar(route.params.id as string, updateData);
    } else {
      await eventoStore.crear(formData.value);
    }

    mostrarExito.value = true;
  } catch (error: any) {
    mensajeError.value = error.message || 'Error al guardar el evento';
  }
};

const volverAtras = () => {
  router.back();
};
</script>

<style scoped>
.form-container {
  padding: 16px;
}

.button-container {
  margin-top: 24px;
}

.imagen-container {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 16px auto;
  cursor: pointer;
}

.imagen-preview {
  width: 100%;
  max-height: 250px;
  object-fit: cover;
  border-radius: 8px;
  display: block;
}

.imagen-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.imagen-container:hover .imagen-overlay {
  opacity: 1;
}

.close-icon {
  font-size: 48px;
  color: white;
}

input[type="file"] {
  margin-top: 8px;
}
</style>
