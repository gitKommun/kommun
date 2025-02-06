<template>
  <div class="flex-1 min-h-0 relative">
    <transition
      enter-active-class="transition-all transition-slow ease-out overflow-hidden"
      leave-active-class="transition-all transition-slow ease-in overflow-hidden"
      enter-class="opacity-0"
      enter-to-class="opacity-100"
      leave-class="opacity-100"
      leave-to-class="opacity-0"
      mode="out-in"
    >
      <div
        v-if="loading"
        class="h-full w-full flex justify-center items-center"
        key="loading"
      >
        <Loading />
      </div>
      <div v-else class="w-full h-full flex flex-col overflow-y-scroll">
        <div
          v-if="!zones.length"
          class="w-full h-full flex flex-col items-center justify-center py-16"
        >
          <PresetZones @update:items="getZones()" />
          <!-- <EmptyTask class="scale-75" />
            <span
              class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300"
            >
              Actualmente no hay áreas comunes
            </span>
            <span class="text-sm text-slate-500 max-w-80 text-center mb-3"
              >Aun no hay registrado ningún elemento como zona comun</span
            >
            <Button
              severity="contrast"
              @click="showCreateZoneModal = true"
              class="flex"
            >
              Crear primer elemento
            </Button> -->
        </div>

        <div v-else class="px-4">
          <div class="w-full flex justify-end py-4">
            <Button
              severity="contrast"
              @click="showCreateZoneModal = true"
              class="flex"
              raised
            >
              <IconPlus />Nueva zona
            </Button>
          </div>
          <div class="mb-3">
            <div class="text-lg font-semibold mb-3">Zonas reservables</div>
            <div
              class="w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 content-start gap-3 pb-4"
            >
              <BookingZone
                v-for="zone in reservableZones"
                :key="zone.area_id"
                :zone="zone"
                @update:item="selectedZone = zone"
              />
            </div>
          </div>
          <div class="text-lg font-semibold mb-3">Otras zonas comunes</div>
          <DataTable
            :value="nonReservableZones"
            paginator
            :rows="20"
            :rowsPerPageOptions="[20, 40, 60, 100]"
            tableStyle="min-width: 50rem"
            class="text-sm"
          >
            <Column field="name" header="Nombre"></Column>
            <Column
              :rowEditor="true"
              style="width: 10%; min-width: 8rem"
              bodyStyle="text-align:right"
            >
              <template #body="slotProps">
                <Dropdown strategy="fixed">
                  <template #reference="{ open }">
                    <div
                      class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer"
                      @click="open"
                    >
                      <IconDotsHorizontal class="text-slate-500" />
                    </div>
                  </template>
                  <template #content="{ close }">
                    <div
                      class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm"
                    >
                      <div
                        class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
                        @click="openUpdateZone(slotProps.data)"
                      >
                        <IconPencil class="scale-75" />
                        <span>Editar</span>
                      </div>
                      <div
                        class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                        @click="deleteZone(slotProps.data.area_id)"
                      >
                        <IconTrash class="scale-75" />
                        <span>Eliminar</span>
                      </div>
                    </div>
                  </template>
                </Dropdown>
              </template>
            </Column>
          </DataTable>
        </div>
        <!-- detalle -->
        <div
          class="absolute top-0 right-0 h-full transition-all duration-300 bounce-transition"
          :class="{ 'w-full md:w-96': openDetail, 'w-0 ': !openDetail }"
        >
          <transition
            enter-active-class="transition-all transition-slow ease-out overflow-hidden"
            leave-active-class="transition-all transition-slow ease-in overflow-hidden"
            enter-class="opacity-0 ml-2"
            enter-to-class="opacity-100 ml-0"
            leave-class="opacity-100 ml-0"
            leave-to-class="opacity-0 ml-2"
          >
            <div
              v-if="openDetail"
              class="w-full h-full bg-white rounded-xl shadow-2xl p-3 flex flex-col"
            >
              <div class="w-full flex items-center">
                <span class="w-full text-sm text-slate-500 uppercase truncate"
                  >Zona -
                  <span class="text-indigo-500">{{
                    selectedZone.area_id
                  }}</span>
                </span>
                <div
                  class="min-h-10 min-w-10 rounded-xl hover:bg-slate-50 flex items-center justify-center transition-all duration-300 group"
                  @click="openDetail = false"
                >
                  <IconClose
                    class="group-hover:rotate-90 transition-all duration-300"
                    @click="selectedZone = null"
                  />
                </div>
              </div>
              <div class="flex flex-col py-3">
                <div class="font-bold truncate text-lg mb-3">
                  {{ selectedZone.name }}
                </div>
                <span class="text-slate-500 text-sm mb-2"
                  >Fecha de reserva:</span
                >
                <DatePicker
                  v-model="bookDate"
                  dateFormat="dd/mm/yy"
                  inputId="on_label"
                  showIcon
                  iconDisplay="input"
                  variant="filled"
                  class="w-full"
                />
              </div>
              <span class="text-slate-500 uppercase text-xs mb-2 py-2"
                >Horarios</span
              >
              <div class="flex-1 min-h-0 overflow-y-scroll g">
                <SlotZone
                  v-for="(slot, i) in demoSlots"
                  :key="i"
                  :slot="slot"
                  class="mb-2"
                />
              </div>
            </div>
          </transition>
        </div>

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
        <Dialog
          v-model:visible="showUpdateZone"
          modal
          header="Editar zona"
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
                La zona tiene que ser reservada por los propitarios
              </span>
            </div>
            <transition
              enter-active-class="transition-all transition-slow ease-out overflow-hidden"
              leave-active-class="transition-all transition-slow ease-in overflow-hidden"
              enter-class="opacity-0"
              enter-to-class="opacity-100"
              leave-class="opacity-100"
              leave-to-class="opacity-0"
              mode="out-in"
            >
              <div class="mt-3 rounded-xl p-3" v-if="zone.reservable">
                <span class="text-slate-500 text-sm"
                  >Define la franja de tiempo para el uso de la zona:</span
                >
                <div class="flex gap-x-3 py-3">
                  <InputGroup>
                    <InputNumber
                      v-model="zone.reservation_duration"
                      placeholder="Tiempo"
                      inputClass="w-12 mr-1"
                      variant="filled"
                    />
                    <Select
                      v-model="zone.time_unit"
                      :options="timePeriods"
                      optionLabel="label"
                      optionValue="value"
                      placeholder="Selecciona..."
                      variant="filled"
                    />
                  </InputGroup>
                </div>
              </div>
            </transition>
          </div>

          <div class="flex justify-end gap-x-4 pt-4">
            <Button text severity="secondary" @click="!showUpdateZone">
              Cancelar
            </Button>
            <Button severity="contrast" @click="updateZone()">
              Actualizar
            </Button>
          </div>
        </Dialog>
      </div>
    </transition>
  </div>
</template>
<script setup>
import { ref, onMounted, computed, watch } from "vue";
import Main from "/src/layouts/Main.vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useRouter } from "vue-router";
import { useConfirm } from "primevue/useconfirm";
import Loading from "/src/components/Loading.vue";
import EmptyTask from "/src/components/emptys/EmptyTask.vue";
import IconPlus from "/src/components/icons/IconPlus.vue";
import IconDotsHorizontal from "/src/components/icons/IconDotsHorizontal.vue";
import IconPencil from "/src/components/icons/IconPencil.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";
import Dropdown from "/src/components/Dropdown.vue";
import PresetZones from "/src/components/zones/PresetZones.vue";
import BookingZone from "/src/components/zones/BookingZone.vue";
import IconClose from "/src/components/icons/IconClose.vue";
import SlotZone from "/src/components/zones/SlotZone.vue";

defineOptions({
  name: "Zones",
  layout: Main,
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const route = useRouter();
const confirm = useConfirm();

//variables
const loading = ref(true);
const zones = ref([]);
const showCreateZoneModal = ref(false);
const showUpdateZone = ref(false);
const zonesNameValidation = ref(true);
const openDetail = ref(false);
const zone = ref({
  name: "",
  reservable: false,
  reservation_duration: 0,
  time_unit: "",
});
const timePeriods = ref([
  { label: "Minutos", value: "MIN" },
  { label: "Horas", value: "HOUR" },
  { label: "Día Completo", value: "DAY" },
]);
const selectedZone = ref(null);
const bookDate = ref(new Date());

const demoSlots = ref([
  {
    slot_start: "2025-10-01T10:00:00",
    slot_end: "2025-10-01T11:30:00",
    reservation: true,
    user: "Jose Plaza",
  },
  {
    slot_start: "2025-10-01T11:30:00",
    slot_end: "2025-10-01T13:00:00",
    reservation: false,
  },
  {
    slot_start: "2025-10-01T13:00:00",
    slot_end: "2025-10-01T14:30:00",
    reservation: false,
  },
]);

const getZones = async () => {
  try {
    const response = await http.get(
      `common_areas/${user?.current_community?.community_id}/`
    );
    zones.value = response.data;
    loading.value = false;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
};
getZones();

//createZone
const createZone = () => {
  if (zone.name != "") {
    zonesNameValidation.value = true;
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
      updateItems();
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
    zonesNameValidation.value = false;
  }
};

//editZone
const openUpdateZone = (item) => {
  showUpdateZone.value = true;
  zone.value = item;
};
const updateZone = () => {
  try {
    http.put(
      `common_areas/${user?.current_community?.community_id}/${zone.value.area_id}/`,
      zone.value
    );
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "La zona se ha actualizado con exito",
      life: 3000,
    });

    showUpdateZone.value = false;
    zone.value = {
      name: "",
      reservable: false,
      reservation_duration: 0,
      time_unit: "",
    };
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
  updateItems();
};

//deleteZone
const deleteZone = (id) => {
  try {
    http.delete(`common_areas/${user?.current_community?.community_id}/${id}/`);
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "La zona se ha eliminado con exito",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
  updateItems();
};

const reservableZones = computed(() => {
  return zones.value.filter((zone) => zone.reservable);
});

const nonReservableZones = computed(() => {
  return zones.value.filter((zone) => !zone.reservable);
});

//miscelanea
function updateItems() {
  setTimeout(() => {
    getZones();
  }, 300);
}

watch(
  selectedZone,
  (newValue, oldValue) => {
    if (!newValue) {
      openDetail.value = false;
    } else {
      openDetail.value = true;
      if (oldValue) {
      }
    }
    openDetail.value = !!newValue;
    console.log("ha cambiado");
  },
  { deep: true }
);
onMounted(() => {
  updateItems();
});
</script>
