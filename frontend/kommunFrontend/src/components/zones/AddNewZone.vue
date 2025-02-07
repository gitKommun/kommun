<template>
    <div class="">
        <Button
              severity="contrast"
              @click="showCreateZoneModal = true"
              class="flex"
              raised
            >
              <IconPlus />Nueva zona
            </Button>
                    <Dialog
          v-model:visible="showCreateZoneModal"
          modal
          header="Crear nueva zona"
          class="w-96"
        >
          <div class="gap-y-2">
            <InputText
              v-model="zone.name"
              placeholder="Nombre de la zona"
              class="w-full"
              variant="filled"
            />
            <div class="flex items-center mt-6">
              <span class="min-w-10">
                <ToggleSwitch v-model="zone.reservable" />
              </span>
              <span class="ml-3">
                La zona que puede ser reservada por los propitarios
              </span>
            </div>
            <transition
              enter-active-class="transition-all transition-slow ease-out overflow-hidden"
              leave-active-class="transition-all transition-slow ease-in overflow-hidden"
              enter-class="opacity-0"
              enter-to-class="opacity-100"
              leave-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <div class="mt-3 rounded-xl p-3">
                <span class="text-slate-500 text-sm"
                  >Define la franja de tiempo para el uso de la zona:</span
                >
                <div class="flex gap-x-3 py-3">
                  <InputGroup>
                    <InputNumber
                      v-model="zone.reservation_duration"
                      placeholder="Tiempo"
                      variant="filled"
                      inputClass="w-12 mr-1"
                      :disabled="!zone.reservable"
                    />
                    <Select
                      v-model="zone.time_unit"
                      :options="timePeriods"
                      optionLabel="label"
                      optionValue="value"
                      variant="filled"
                      placeholder="Selecciona..."
                      :disabled="!zone.reservable"
                    />
                  </InputGroup>
                </div>
              </div>
            </transition>
          </div>

          <div class="flex justify-end gap-x-4 pt-4">
            <Button
              text
              severity="secondary"
              @click="showCreateZoneModal = !showCreateZoneModal"
            >
              Cancelar
            </Button>
            <Button severity="contrast" @click="createZone"> Crear </Button>
          </div>
        </Dialog>
    </div>
</template>
<script setup>
import { ref, watch, computed} from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from "primevue/useconfirm";
import IconPlus from "/src/components/icons/IconPlus.vue";

defineOptions({
    name: 'AddNewZone',
})

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const emit = defineEmits(['update:zones']);

//variables
const showCreateZoneModal = ref(false);
const zone = ref({
    name: '',
    reservable: false,
    reservation_duration: '',
    time_unit: '',
    area_id: null,
})
const timePeriods = ref([
    { label: 'Minutos', value: 'MIN' },
    { label: 'Horas', value: 'HOUR' },
    { label: 'Día Completo', value: 'DAY' }
])

const createZone = () => {
  if (zone.name != "") {
    try {
      http.post(
        `common_areas/${user?.current_community?.community_id}/create/`,
        zone.value
      );

      toast.add({
        severity: "success",
        summary: "Ok",
        detail: "Zona creada con exito",
        life: 3000,
      });
      emit("update:zones", true);
    } catch (error) {
      toast.add({
        severity: "error",
        summary: "Upps!! algo ha fallado",
        detail: error,
        life: 3000,
      });
    }
    zone.value = {
      name: "",
      reservable: false,
      reservation_duration: "",
      time_unit: "",
    };
    showCreateZoneModal.value = false;
  } else {
    toast.add({
        severity: "error",
        summary: "Upps!! El nombre no puede estar vacío",
        detail: error,
        life: 3000,
      });
  }
};
</script>
