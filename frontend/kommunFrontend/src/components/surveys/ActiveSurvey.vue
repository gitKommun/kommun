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
        <Button severity="contrast" size="small">Votar</Button>
      </div>
    </div>
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

const isDelegated = ref(true);
const iAmDelegated = ref(false);

const dateFormat = (itemDate) => {
  const date = new Date(itemDate);
  const day = String(date.getDate()).padStart(2, "0"); // Día con dos dígitos
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Mes con dos dígitos
  const year = date.getFullYear(); // Año completo
  return `${day}/${month}/${year}`;
};
</script>
