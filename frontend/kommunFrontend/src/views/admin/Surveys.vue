<template>
  <div class="flex-1 min-h-0 overflow-y-scroll relative px-4">
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
        class="h-full w-full flex flex-col pt-3 overflow-y-scroll relative"
        key="content"
      >
        <div class="flex justify-between items-center py-4">
          <InputText
            v-model="search"
            placeholder="Buscar"
            size="small"
            variant="filled"
          />
          <AddNewSurvey @update:surveys="updateItems" class="h-auto" />
        </div>
        <div class="px-4 min-h-0 flex-1" v-if="!surveys.length">
          <div class="w-full flex flex-col items-center justify-center py-24">
            <EmptyTask class="scale-75" />
            <span
              class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300"
            >
              Actualmente no hay votaciones
            </span>
            <!-- <span class="text-sm text-slate-500 max-w-100 text-center"
              >Indica la referencia catastral de la propiedad que deseas cargar
              y apareceran automaticamente</span
            > -->
          </div>
        </div>
        <div v-else class="px-4 min-h-0 flex-1">
          <!-- content -->

          <div class="mb-3">
            <div class="text-lg font-semibold mb-3">Votaciones en curso</div>
            <div class="w-full gap-3 pb-4">
              <ActiveSurvey
                :survey="survey"
                v-for="survey in getMyOpenSurveys"
                :key="survey.vote_id"
              />
            </div>
          </div>
          <div class="mt-2">
            <DataTable
              v-model:selection="selectedSurvey"
              selectionMode="single"
              :value="filteredSurveys"
              paginator
              :rows="20"
              :rowsPerPageOptions="[20, 40, 60, 100]"
              tableStyle="min-width: 50rem"
              class="text-xs"
            >
              <Column field="title" sortable header="Título"></Column>
              <Column
                field="start_date"
                dataType="date"
                sortable
                header="Inicio"
              >
                <template #body="slotProps">
                  {{ formatDate(slotProps.data.start_date) }}
                </template>
              </Column>
              <Column field="end_date" sortable header="Fin">
                <template #body="slotProps">
                  {{ formatDate(slotProps.data.end_date) }}
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
                        :style="{
                          width: `${getProcess(slotProps.data.users)}`,
                        }"
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
                    <span class="text-indigo-500">{{
                      selectedSurvey.vote_id
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
          <!-- content -->
        </div>
      </div>
    </transition>

    <Toast />
  </div>
</template>
<script setup>
import { computed, ref, watch } from "vue";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useRouter } from "vue-router";
import { useHttp } from "/src/composables/useHttp.js";
import { formatDate } from "@/utils/dateUtils";
import Main from "/src/layouts/Main.vue";
import AddNewSurvey from "/src/components/surveys/AddNewSurvey.vue";
import IconClose from "/src/components/icons/IconClose.vue";
import HighChart from "@/components/HighChart.vue";
import ActiveSurvey from "/src/components/surveys/ActiveSurvey.vue";
import EmptyTask from "/src/components/emptys/EmptyTask.vue";
import Loading from "@/components/Loading.vue";

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
const search = ref("");
const loading = ref(true);

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
  loading.value = false;
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
  return surveys.value
    .filter(survey => survey.status === "open")
    .flatMap(survey => {
      const mySurveys = [];
      
      // Buscar si soy participante directo
      const myDirectParticipation = survey.users.find(
        userObj => userObj.person_community_id === user?.current_community?.community_person_id
      );
      
      // Si soy participante directo, añadir la survey con mi usuario
      if (myDirectParticipation) {
        mySurveys.push({
          ...survey,
          users: myDirectParticipation,
          participationType: 'direct'
        });
      }
      
      // Buscar todos los usuarios que me han delegado su voto
      const delegatedToMe = survey.users.filter(
        userObj => 
          userObj.delegate_to?.person_community_id === user?.current_community?.community_person_id
      );
      
      // Añadir una entrada por cada delegación
      delegatedToMe.forEach(delegator => {
        mySurveys.push({
          ...survey,
          users: delegator,
          participationType: 'delegated'
        });
      });
      
      return mySurveys;
    });
});

const getProcess = (users) => {
  const total = users.length;

  const answers = users.filter((user) => user.answer !== null).length;

  return (answers * 100) / total;
};


//funcion para buscar surveys
const filteredSurveys = computed(() => {
  return surveys.value.filter((survey) => {
    return survey.title.toLowerCase().includes(search.value.toLowerCase());
  });
});

function updateItems() {
  setTimeout(() => {
    getSurveys();
  }, 300);
}

</script>
