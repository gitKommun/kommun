<template>
  <div class="w-full rounded-xl border border-slate-200 p-3">
    <LoadProperties v-if="!hasProperties" @update:loaded="updateProperties" />
    <div v-else class="flex flex-col md:flex-row gap-y-3 md:gap-y-0 md:gap-x-3 mb-4">
      <div
        v-for="prop in groupedData"
        :key="prop.key"
        class="w-full flex md:flex-col justify-between md:justify-center items-center bg-slate-100 rounded-xl p-3"
      >
        <span class="uppercase text-xs md:mb-2" :class="`text-[${prop.color}]`">
          {{ prop.label }}
        </span>
        <span class="font-bold text-lg">{{ prop.count }}</span>
      </div>
    </div>
    <div v-if="hasProperties" class="w-full py-2 text-sm mb-4">
      <span class="text-xs text-slate-400 mb-2"
        >Propiedades por superficie</span
      >
      <MeterGroup :value="groupedData" />
    </div>
    <Toast />
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { USAGES_HEX } from "/src/constants/colors.js";
import LoadProperties from "/src/components/properties/LoadProperties.vue";

defineOptions({
  name: "PropertiesDetails",
});
const props = defineProps({
  community: {
    type: Object,
  },
  hasProperties: {
    type: Boolean,
  },
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

//emit
const emit = defineEmits(["update:loaded"]);

//variables
const properties = ref([]);


const getProperties = async () => {
  try {
    const response = await http.get(
      `properties/${user?.current_community?.community_id}/`
    );
    properties.value = response.data;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
};

const updateProperties = () => {
  getProperties();
  emit("update:properties", true);
};

getProperties();


//miscelanea
const groupedData = computed(() => {
  const usageCount = {};
  const usageArea = {};
  let totalSurfaceArea = 0;

  // Agrupar y sumar superficie total
  properties.value.forEach((property) => {
    const usage = property.usage;
    const surfaceArea = parseFloat(property.surface_area);

    if (!usageCount[usage]) {
      usageCount[usage] = 0;
      usageArea[usage] = 0;
    }

    usageCount[usage] += 1;
    usageArea[usage] += surfaceArea;
    totalSurfaceArea += surfaceArea;
  });

  // Formatear los resultados para la salida esperada
  return Object.keys(usageCount).map((key) => {
    return {
      label: key,
      color:
        key === "ALMACEN-ESTACIONAMIENTO"
          ? USAGES_HEX.ALMACEN_ESTACIONAMIENTO
          : USAGES_HEX[key] || "#000000", // Color por defecto si no está en el objeto
      value: ((usageArea[key] / totalSurfaceArea) * 100).toFixed(2), // Porcentaje basado en surface_area,
      count: usageCount[key],
    };
  });
});
</script>
