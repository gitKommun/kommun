<template>
  <div class="h-full w-full">
    <div class="flex justify-between items-center mb-3 px-3">
      <InputText
        v-model="search"
        placeholder="Buscar"
        size="small"
        variant="filled"
      />
      <AddNewSurvey @update:items="updateItems" class="h-auto" />
    </div>
    <div class="w-full px-3 flex-1 min-h-0 overflow-y-scroll">
      <DataTable
        :value="surveys"
        paginator
        scrollHeight="700px"
        scrollable
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
          {{ dateFormat(slotProps.data.start_date) }}
        </template>
      </Column>
        <Column field="end_date" sortable header="Fin">
        <template #body="slotProps">
          {{ dateFormat(slotProps.data.end_date) }}
        </template>
        </Column>
        <Column header="Audiencia"></Column>
        <Column header="Progreso"></Column>
      </DataTable>
    </div>
    <Toast />
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useRouter } from "vue-router";
import { useHttp } from "/src/composables/useHttp.js";

import Main from "/src/layouts/Main.vue";
import AddNewSurvey from "/src/components/surveys/AddNewSurvey.vue";

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

const getSurveys = async () => {
  try {
    const response = await http.get(
      `votes/${user?.current_community?.community_id}/polls/`
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

const dateFormat = (itemDate) => {
  const date = new Date(itemDate);
  const day = String(date.getDate()).padStart(2, "0"); // Día con dos dígitos
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Mes con dos dígitos
  const year = date.getFullYear(); // Año completo
  return `${day}/${month}/${year}`;
};
</script>
