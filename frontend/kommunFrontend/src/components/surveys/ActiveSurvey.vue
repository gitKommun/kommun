<template>
  <div
    class="flex flex-col items-start border p-3 rounded-2xl gap-x-3 mb-3 w-full relative transition-all duration-300"
  >
    <div class="text-slate-500 text-xs">
      <span>HASTA: {{ dateFormat(survey.start_date) }}</span>
    </div>
    <div class="w-full flex font-bold mb-2">
      {{ survey.title }}
    </div>
    <div class="w-full flex justify-between items-center">
      <div class="text-slate-500 text-sm">
        <!-- soy delegado -->
        <template v-if="isDelegated">
          <CustomAvatar :name="'juan Palomo'" size="small" />
          <span class="text-sm text-slate-500"> Juan Palomo </span>
          <span>te ha delegado su voto</span>
        </template>
        <!-- me han delegado -->
        <template v-if="iAmDelegated">
          <span class="mr-1">Voto delegado a</span>
          <CustomAvatar :name="'juan Palomo'" size="small" />
          <span class="text-sm text-slate-500"> Juan Palomo </span>
        </template>
      </div>
      <div class="flex gap-2">
        <Button v-if="!isDelegated" severity="secondary" size="small"
          >Delegar</Button
        >
        <Button @click="showSurvey = true" severity="contrast" size="small">Votar</Button>
      </div>
    </div>
    <Dialog 
      v-model:visible="showSurvey" 
      modal 
      
      header="Votación" 
      class="w-128">
      <div>
        <div class="text-lg font-bold">
          {{ survey.title }}
        </div>
        <div class="text-sm text-slate-500">
          {{ survey.description }}
        </div>
        <div class="py-3 flex flex-col gap-2">
          <div v-for="(el,index) in 4" :key="index" class="border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50 rounded-lg p-3 w-full transition-all duration-300">
            option {{ index + 1 }}
          </div>
        </div>
      </div>
    </Dialog>
  </div>
</template>
<script setup>
import { ref } from "vue";
import CustomAvatar from "/src/components/CustomAvatar.vue";

defineOptions({
  name: "ActiveSurvey",
});

const props = defineProps({
  survey: {
    type: Object,
  },
});

const isDelegated = ref(false);
const iAmDelegated = ref(false);
const showSurvey = ref(false);

const dateFormat = (itemDate) => {
  const date = new Date(itemDate);
  const day = String(date.getDate()).padStart(2, "0"); // Día con dos dígitos
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Mes con dos dígitos
  const year = date.getFullYear(); // Año completo
  return `${day}/${month}/${year}`;
};
</script>
