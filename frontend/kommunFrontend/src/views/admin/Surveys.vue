<template>
  <div class="flex-1 min-h-0 overflow-y-scroll relative px-4">
    <div class="flex justify-between items-center py-4">
      <InputText
        v-model="search"
        placeholder="Buscar"
        size="small"
        variant="filled"
      />
      <AddNewSurvey @update:surveys="updateItems" class="h-auto" />
    </div>
    <div class="mb-3">
      <div class="text-lg font-semibold mb-3">Votaciones en curso</div>
      <div
        class="w-full  gap-3 pb-4"
      >
      <ActiveSurvey 
        :survey="survey" 
        v-for="survey in getMyOpenSurveys" 
        :key="survey.vote_id"/>
        <!-- <BookingZone
                v-for="zone in reservableZones"
                :key="zone.area_id"
                :zone="zone"
                @update:item="selectedZone = zone"
                @update:delete="deleteZone(zone.area_id)"
                @update:edit="openUpdateZone(zone)"
              /> -->
      </div>
    </div>
    <div class="mt-2">
      <DataTable
        v-model:selection="selectedSurvey"
        selectionMode="single"
        :value="surveys"
        paginator
        :rows="20"
        :rowsPerPageOptions="[20, 40, 60, 100]"
        tableStyle="min-width: 50rem"
        class="text-xs"
      >
        <Column field="title" sortable header="Título"></Column>
        <Column field="start_date" dataType="date" sortable header="Inicio">
          <template #body="slotProps">
            {{ dateFormat(slotProps.data.start_date) }}
          </template>
        </Column>
        <Column field="end_date" sortable header="Fin">
          <template #body="slotProps">
            {{ dateFormat(slotProps.data.end_date) }}
          </template>
        </Column>
        <Column header="Audiencia">
          <template #body="slotProps">
            {{ slotProps.data.users.length }}
          </template>
        </Column>
        <Column header="Progreso">
          <template #body="slotProps">
            <div class="flex items-center gap-x-2">
              <div
                class="h-2 w-20 bg-slate-200 relative rounded-[3px] overflow-hidden"
              >
                <div
                  class="h-full bg-green-500 absolute top-0 left-0 transition-all duration-300 group-hover:w-full"
                  :style="{ width: `${getProcess(slotProps.data.users)}` }"
                ></div>
              </div>
              <span>{{ getProcess(slotProps.data.users) }}%</span>
            </div>
          </template>
        </Column>
      </DataTable>
    </div>
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
              >Votación -
              <span class="text-indigo-500">{{ selectedSurvey.vote_id }}</span>
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
          <!-- chart -->
          <div class="p-3 border border-200 rounded-2xl">
            <p class="font-bold text-lg mb-3">
              {{ selectedSurvey?.title }}
            </p>
            <div class="bg-red-100 h-56 flex justify-center items-center">
              <HighChart :options="demoData" />
            </div>
          </div>
          <!-- ansewers -->
          <div class="text-slate-500 text-xs my-3">
            <span class="uppercase text-xs mr-1">Respuestas</span>
          </div>
          <div class="flex-1 min-h-0 overflow-y-scroll py-3">
            <div
              v-for="(e, i) in 20"
              :key="i"
              class="px-3 py-2 border-l-4 border-blue-500 mb-[4px] text-sm"
            >
              Nombre de vecino
            </div>
          </div>
        </div>
      </transition>
    </div>
    <Toast />

  </div>
</template>
<script setup>
import { computed, ref, watch } from "vue";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useRouter } from "vue-router";
import { useHttp } from "/src/composables/useHttp.js";

import Main from "/src/layouts/Main.vue";
import AddNewSurvey from "/src/components/surveys/AddNewSurvey.vue";
import IconClose from "/src/components/icons/IconClose.vue";
import HighChart from "@/components/HighChart.vue";
import ActiveSurvey from "/src/components/surveys/ActiveSurvey.vue";


defineOptions({
  name: "surveys",
  layout: Main,
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const route = useRouter();

//variables
const surveys = ref([]);
const selectedSurvey = ref(null);
const openDetail = ref(false);

const getSurveys = async () => {
  try {
    const response = await http.get(
      `votes/${user?.current_community?.community_id}/`
    );
    surveys.value = response.data;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
};
getSurveys();

watch(
  selectedSurvey,
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

const demoData = {
  chart: {
    type: "bar",
  },
  plotOptions: {
    bar: {
      borderRadius: "20%",
      dataLabels: {
        enabled: true,
      },
      groupPadding: 0.1,
    },
  },
  xAxis: {
    labels: {
      enabled: false,
    },
  },
  series: [
    {
      name: "Si",
      data: [34],
    },
    {
      name: "No",
      data: [20],
    },
    {
      name: "Abstención",
      data: [12],
    },
  ],
};

// funcion computada para devolver las surveys que están abiertas y en las cuales estoy como user o como delegado

const getMyOpenSurveys = computed(() => {
  return surveys.value.filter(
    survey =>
      survey.status === "open" &&
      survey.users.some(userObj => userObj.person_community_id === user?.current_community?.community_person_id) //si soy el asignado
    // survey.users.some(userObj => userObj.delegate_to.user_id === user?.current_community?.community_person_id) //si me lo han delegado
  );
});

const getProcess = (users) => {
  const total = users.length;

  const answers = users.filter((user) => user.answer !== null).length;

  return (answers * 100) / total;
};


function updateItems() {
  setTimeout(() => {
    getSurveys();
  }, 300);
}

const dateFormat = (itemDate) => {
  const date = new Date(itemDate);
  const day = String(date.getDate()).padStart(2, "0"); // Día con dos dígitos
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Mes con dos dígitos
  const year = date.getFullYear(); // Año completo
  return `${day}/${month}/${year}`;
};
</script>
