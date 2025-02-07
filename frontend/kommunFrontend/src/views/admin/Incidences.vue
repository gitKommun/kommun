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
      <div
        v-else
        class="h-full w-full flex flex-col overflow-y-scroll"
        key="content"
      >
        <div class="px-4 min-h-0 flex-1" v-if="!incidences.length">
          <div class="w-full flex flex-col items-center justify-center py-24">
            <EmptyTask class="scale-75" />
            <span
              class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300"
            >
              Actualmente no hay incidencias
            </span>
            <span class="text-sm text-slate-500 max-w-100 text-center mb-6"
              >Si lo deseas, puedes crear una nueva incidencia</span
            >
            <AddNewIncidence @update:items="updateItems" class="h-auto" />
          </div>
        </div>
        <div v-else class="min-h-0 flex-1">
          <!-- toolbar -->
          <div class="w-full p-4 flex justify-between">
            <InputText
              v-model="search"
              placeholder="Buscar"
              size="small"
              variant="filled"
            />
            <AddNewIncidence @update:items="updateItems" class="h-auto" />
          </div>
          <!-- últimas incidencias -->
          <div class="px-4">
            <div class="text-lg font-semibold mb-3">
              Últimas incidencias reportadas
            </div>
            <div
              class="w-full gap-2 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 mb-3"
            >
              <template v-for="(incidence, index) in incidences">
                <LastIncidenceItem
                  v-if="index < 3"
                  :key="'#' + index"
                  :incidence="incidence"
                  @click="selectedIncidence = incidence"
                />
              </template>
            </div>
          </div>
          <!-- tabla de incidencias -->
          <div class="px-4">
            <DataTable
              v-model:selection="selectedIncidence"
              selectionMode="single"
              paginator
              :rows="20"
              :rowsPerPageOptions="[20, 40, 60, 100]"
              :value="incidences"
              tableStyle="min-width: 50rem"
              class="text-sm"
            >
              <Column field="title" header="Incidencia">
                <template #body="slotProps">
                  <span class="flex items-center truncate">
                    <IconFlag
                      class="scale-75 mr-2"
                      :class="`text-${
                        PRIORITY_COLOR[slotProps.data.priority]
                      }-500`"
                    />{{ slotProps.data.title }}</span
                  >
                </template>
              </Column>
              <column header="Fecha">
                <template #body="slotProps">
                  <span>{{ dateFormat(slotProps.data.created_at) }}</span>
                </template>
              </column>
              <column header="Estado">
                <template #body="slotProps">
                  <CustomTag
                    :color="INCIDENCE_STATUS_COLOR[slotProps.data.status]"
                  >
                    {{ INCIDENCE_STATUS_LABEL[slotProps.data.status] }}
                  </CustomTag>
                </template>
              </column>
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
                    >Incidencia -
                    <span class="text-indigo-500">{{
                      selectedIncidence.claim_id
                    }}</span>
                  </span>
                  <div
                    class="min-h-10 min-w-10 rounded-xl hover:bg-slate-50 flex items-center justify-center transition-all duration-300 group"
                    @click="openDetail = false"
                  >
                    <IconClose
                      class="group-hover:rotate-90 transition-all duration-300"
                      @click="selectedIncidence = null"
                    />
                  </div>
                </div>
                <!-- incidence card -->
                <div class="border border-slate-200 p-3 rounded-2xl relative">
                  <div class="flex justify-between items-center">
                    <span class="text-slate-500 text-sm">{{
                      dateFormat(selectedIncidence?.created_at)
                    }}</span>
                    <div class="flex gap-x-2">
                      <Dropdown strategy="fixed">
                        <template #reference="{ open }">
                          <div
                            class="border border-slate-200 rounded-lg flex pl-1 items-center"
                            @click="open"
                          >
                            <CustomTag
                              class="mr-1"
                              :color="
                                INCIDENCE_STATUS_COLOR[
                                  selectedIncidence?.status
                                ]
                              "
                              >{{
                                INCIDENCE_STATUS_LABEL[
                                  selectedIncidence?.status
                                ]
                              }}</CustomTag
                            >
                            <div
                              class="size-8 flex items-center justify-center border-l border-slate-200 cursor-pointer"
                            >
                              <IconChevronDown
                                class="scale-75 text-slate-500"
                              />
                            </div>
                          </div>
                        </template>
                        <template #content="{ close }">
                          <div
                            class="w-40 rounded-2xl bg-white p-3 shadow-2xl text-sm flex flex-col"
                          >
                            <div
                              v-for="(el, index) in incidenceStatusOptions"
                              :key="index"
                              class="flex hover:bg-slate-50 p-1 rounded-lg cursor-pointer"
                              @click="selectedIncidence.status = el"
                            >
                              <CustomTag
                                :color="INCIDENCE_STATUS_COLOR[el]"
                                class="flex"
                                >{{ INCIDENCE_STATUS_LABEL[el] }}</CustomTag
                              >
                            </div>
                          </div>
                        </template>
                      </Dropdown>
                      <Dropdown strategy="fixed">
                        <template #reference="{ open }">
                          <div
                            class="size-8 rounded-lg hover:bg-slate-50 transition-all duration-300 flex items-center justify-center cursor-pointer"
                            @click="open"
                          >
                            <IconDots class="text-slate-500" />
                          </div>
                        </template>
                        <template #content="{ close }">
                          <div
                            class="w-56 rounded-2xl bg-white p-3 shadow-2xl text-sm flex flex-col"
                          >
                            <div
                              class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
                            >
                              <IconWorker class="scale-75" />
                              <span>Asignar proveedor</span>
                            </div>
                            <div
                              @click="confirmDelete"
                              class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                            >
                              <IconTrash class="scale-75" />
                              <span>Eliminar</span>
                            </div>
                          </div>
                        </template>
                      </Dropdown>
                    </div>
                  </div>
                  <p
                    class="font-bold text-lg mb-3 line-clamp-2 hover:line-clamp-none transition-all duration-300"
                  >
                    {{ selectedIncidence?.title }}
                  </p>
                  <p
                    class="text-slate-500 text-sm mb-3 line-clamp-2 hover:line-clamp-none transition-all duration-300"
                  >
                    {{ selectedIncidence?.description }}
                  </p>
                  <div class="flex flex-col text-sm text-slate-500">
                    <span>
                      <span class="uppercase text-xs mr-1">Lugar:</span> Sin
                      ubicación</span
                    >
                    <span
                      ><span class="uppercase text-xs mr-1">Categoria:</span
                      >{{
                        INCIDENCE_CATEGORY_LABEL[selectedIncidence?.category]
                      }}</span
                    >
                  </div>
                </div>
                <!-- timeline -->
                <div class="flex-1 min-h-0 py-3 flex flex-col">
                  <div class="text-slate-500 text-xs mb-3">
                    <span class="uppercase text-xs mr-1">Timeline</span>
                  </div>
                  <div class="flex-1 min-h-0 overflow-y-scroll">
                    <div
                      class="flex gap-x-2 text-sm"
                      v-for="(el, index) in demoItem.timeline"
                      :key="index"
                    >
                      <div
                        class="w-6 flex flex-col items-center"
                        :class="
                          index == demoItem.timeline.length - 1
                            ? 'justify-start'
                            : 'justify-center'
                        "
                      >
                        <div
                          class="w-6 h-6 min-h-6 min-w-6 rounded-full border-2 border-slate-200 flex items-center justify-center"
                        >
                          <div
                            class="w-2 h-2 rounded-full"
                            :class="
                              index == demoItem.timeline.length - 1
                                ? 'bg-green-500'
                                : 'bg-slate-900'
                            "
                          ></div>
                        </div>
                        <div
                          v-if="index != demoItem.timeline.length - 1"
                          class="w-[2px] h-full bg-slate-200"
                        ></div>
                      </div>
                      <div class="">
                        <component
                          :is="TIMELINE_EVENT_TYPES[el.event_type]"
                          :item="el"
                        ></component>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- commentarios -->
                <div class="pt-3">
                  <textarea
                    v-model="comment"
                    class="w-full bg-slate-100 rounded-xl p-3 text-sm"
                    placeholder="Comentarios"
                  ></textarea>
                  <Button
                    @click="addMessage()"
                    class="w-full mt-2"
                    label="enviar"
                    severity="contrast"
                    raised
                  />
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </transition>

    <Toast />
    <ConfirmDialog></ConfirmDialog>
  </div>
</template>
<script setup>
import { ref, watch } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";

import Main from "/src/layouts/Main.vue";
import IconClose from "/src/components/icons/IconClose.vue";
import AddNewIncidence from "/src/components/incidences/AddNewIncidence.vue";
import LastIncidenceItem from "/src/components/incidences/LastIncidenceItem.vue";
import CustomTag from "@/components/CustomTag.vue";
import IconFlag from "@/components/icons/IconFlag.vue";
import IconDots from "/src/components/icons/IconDots.vue";
import IconPencil from "/src/components/icons/IconPencil.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";
import IconWorker from "@/components/icons/IconWorker.vue";
import Dropdown from "/src/components/Dropdown.vue";
import IncidenceTimelineContact from "/src/components/incidences/IncidenceTimelineContact.vue";
import IncidenceTimelineMessage from "/src/components/incidences/IncidenceTimelineMessage.vue";
import IncidenceTimelineStatus from "/src/components/incidences/IncidenceTimelineStatus.vue";
import Loading from "@/components/Loading.vue";
import EmptyTask from "/src/components/emptys/EmptyTask.vue";

import {
  PRIORITY_COLOR,
  INCIDENCE_STATUS_COLOR,
} from "/src/constants/colors.js";
import IconChevronDown from "@/components/icons/IconChevronDown.vue";
import {
  INCIDENCE_STATUS_LABEL,
  INCIDENCE_CATEGORY_LABEL,
} from "/src/constants/labels.js";

defineOptions({
  name: "incidences",
  layout: Main,
});

//variables
const incidences = ref([]);
const openDetail = ref(false);
const selectedIncidence = ref(null);
const incidenceStatusOptions = ref([
  "reported",
  "in_process",
  "resolved",
  "closed",
]);
const loading = ref(true);

const TIMELINE_EVENT_TYPES = {
  status: IncidenceTimelineStatus,
  message: IncidenceTimelineMessage,
  provider: IncidenceTimelineContact,
};

const comment = ref("");
const demoItem = {
  claim_id: "",
  title: "",
  description: "",
  create_at: "",
  create_user: "",
  priority: "",
  status: "",
  zone: {},
  timeline: [
    {
      event_id: "1",
      event_type: "status", // status
      event_date: "12/01/2025 12:00",
      event_old_status: "reported",
      event_new_status: "in_process",
    },
    {
      event_id: "2",
      event_type: "message", // message
      event_date: "12/01/2025 12:00",
      event_text: "Es un texto de ejemplo para ver como se ve en el timeline",
      event_user: {
        name: "Joan Marquez",
      },
    },
    {
      event_id: "3",
      event_type: "provider", // provider
      event_date: "12/01/2025 12:00",
      event_company: "Reparaciones Castillo SL",
      event_contact: {
        phone: "987 666 666",
        email: "marcos@reparacionescastillo.com",
      },
    },
    {
      event_id: "4",
      event_type: "message", // message
      event_date: "12/01/2025 12:00",
      event_text:
        "El proveedor resolvera la incidencia el 13/01/2025 entre las 12:00 y 14:00",
      event_user: {
        name: "Joan Marquez",
      },
    },
  ],
};

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const confirm = useConfirm();

const getIncidences = async () => {
  try {
    const response = await http.get(
      `claims/${user?.current_community?.community_id}/`
    );
    incidences.value = response.data;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
  loading.value = false;
};
getIncidences();

//actualizar incidencia
const updateIncedence = async () => {
  try {
    await http.put(
      `claims/${user?.current_community?.community_id}/${selectedIncidence.value.claim_id}/update/`,
      selectedIncidence.value
    );
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "Incidencia actualizada con exito",
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
};

//borrar incidencia

const confirmDelete = () => {
  confirm.require({
    message:
      "Esta acción no se puede revertir, ¿ Estas seguro de borrar esta incidencia?",
    header: "Confirmación",
    rejectProps: {
      label: "Cancel",
      severity: "secondary",
      outlined: true,
    },
    acceptProps: {
      label: "Borrar",
      severity: "danger",
    },
    accept: () => {
      http.delete(
        `claims/${user?.current_community?.community_id}/${selectedIncidence.value.claim_id}/delete`
      );
      toast.add({
        severity: "success",
        summary: "Ok",
        detail: "La incidencia se ha eliminado con exito",
        life: 3000,
      });
      selectedIncidence.value = null;
      setTimeout(() => {
        getIncidences();
      }, 300);
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Upps!!",
        detail: "No se ha podido eliminar la incidencia",
        life: 3000,
      });
    },
  });
};

//añadir comentario
const addMessage = async () => {
  if (comment.value.trim() === "") {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: "El campo de comentario no puede estar vacio",
      life: 3000,
    });
    return;
  }
  try {
    await http.post(
      `claims/${user?.current_community?.community_id}/${selectedIncidence.value.claim_id}/add_comment/`,
      {
        comment: comment.value,
      }
    );
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "Incidencia actualizada con exito",
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
  comment.value = "";
};

function updateItems() {
  setTimeout(() => {
    getIncidences();
  }, 300);
}

watch(
  selectedIncidence,
  (newValue, oldValue) => {
    if (!newValue) {
      openDetail.value = false;
    } else {
      openDetail.value = true;
      if (oldValue) {
        updateIncedence();
      }
    }
    openDetail.value = !!newValue;
  },
  { deep: true }
);

//miscelanea

function dateFormat(dateString) {
  // Intenta crear un objeto Date directamente desde el string ISO
  const date = new Date(dateString);
  // Verifica si la fecha es válida
  if (isNaN(date.getTime())) {
    console.error("Fecha no válida:", dateString);
    return "Fecha no válida";
  }

  // Formatea la fecha como DD/MM/YYYY
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Los meses en JavaScript son 0-indexados
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}
</script>
