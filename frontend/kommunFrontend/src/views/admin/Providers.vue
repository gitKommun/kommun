<template>
  <div class="flex-1 min-h-0 px-4">
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
        class="h-full w-full flex flex-col pt-3 overflow-y-scroll"
        key="content"
      >
        <div class="border border-slate-200 rounded-2xl p-3 mb-3">
          <div
            class="w-full flex gap-x-2 flex-col md:flex-row overflow-x-scroll"
          >
            <div
              class="flex w-full flex-col gap-y-1 mb-4 bg-slate-100 rounded-xl p-3"
              v-if="getTopRatedProviders.length"
            >
              <span class="uppercase text-xs md:mb-2">Valoraciones</span>
              <div
                v-for="(rate, i) in getRatingDistribution"
                :key="i"
                class="flex items-center gap-x-2"
              >
              <template v-if="rate.rating >= 1">
                <div class="w-44 flex justify-end">
                  <IconStarFill
                    class="scale-50 text-slate-900"
                    v-for="star in rate.rating"
                    :key="rate.rating"
                  />
                </div>
                <div
                  class="w-full h-2 bg-slate-200 relative rounded-sm overflow-hidden"
                >
                  <div
                    class="absolute h-2 bg-slate-500 rounded-sm"
                    :style="{ width: rate.value + '%' }"
                  ></div>
                </div>
                <div class="w-8 text-xs text-slate-500">{{ rate.value }}%</div>
              </template>
                
              </div>
            </div>
            <div
              class="flex w-full flex-col gap-y-3 mb-4 bg-slate-100 rounded-xl p-3"
            >
              <span class="uppercase text-xs md:mb-2">Mejor valorados</span>
              <div
                v-for="(provider, i) in getTopRatedProviders"
                :key="i"
                class="w-full flex items-center rounded-xl"
              >
                <span class="flex items-center gap-x-2">
                  <span
                    :class="`size-8 min-w-8 rounded-lg flex items-center justify-center bg-${
                      PROVIDER_COLOR[provider.type]
                    }-100`"
                  >
                    <component
                      :is="PROVIDER_ICONS[provider.type]"
                      :class="`scale-75 text-${
                        PROVIDER_COLOR[provider.type]
                      }-500`"
                    />
                  </span>
                  <span class="truncate">{{ provider.company_name }}</span>
                </span>
              </div>
            </div>
            <div
              class="flex w-full flex-col gap-y-3 mb-4 bg-slate-100 rounded-xl p-3"
            >
              <span class="uppercase text-xs md:mb-2">Peor valorados</span>
              <div
                v-for="(provider, i) in getWorstRatedProviders"
                :key="i"
                class="w-full flex items-center rounded-xl"
              >
                <span class="flex items-center gap-x-2">
                  <span
                    :class="`size-8 min-w-8 rounded-lg flex items-center justify-center bg-${
                      PROVIDER_COLOR[provider.type]
                    }-100`"
                  >
                    <component
                      :is="PROVIDER_ICONS[provider.type]"
                      :class="`scale-75 text-${
                        PROVIDER_COLOR[provider.type]
                      }-500`"
                    />
                  </span>
                  <span class="truncate">{{ provider.company_name }}</span>
                </span>
              </div>
            </div>
          </div>

          <div class="w-full py-2 text-sm mb-4">
            <span class="text-xs text-slate-400 mb-2"
              >Distribución de proveedores</span
            >
            <MeterGroup :value="providerStats" class="text-sm" />
          </div>
        </div>
        <div class="flex justify-between items-center py-4">
          <InputText
            v-model="search"
            placeholder="Buscar"
            size="small"
            variant="filled"
          />
          <AddNewProvider @update:providers="updateItems" class="h-auto" />
        </div>
        <DataTable
          :value="providers"
          paginator
          :rows="20"
          :rowsPerPageOptions="[20, 40, 60, 100]"
          tableStyle="min-width: 50rem"
          class="text-xs"
        >
          <Column field="company_name" header="Empresa">
            <template #body="slotProps">
              <span class="flex items-center gap-x-2">
                <span
                  :class="`size-8 min-w-8 rounded-lg flex items-center justify-center bg-${
                    PROVIDER_COLOR[slotProps.data.type]
                  }-100`"
                >
                  <component
                    :is="PROVIDER_ICONS[slotProps.data.type]"
                    :class="`scale-75 text-${
                      PROVIDER_COLOR[slotProps.data.type]
                    }-500`"
                  />
                </span>
                <span class="">{{ slotProps.data.company_name }}</span>
              </span>
            </template>
          </Column>
          <Column field="phone" header="Teléfono"></Column>
          <Column field="email" header="Correo electrónico"></Column>
          <Column field="address" header="Dirección"></Column>
          <Column field="rating" header="Valoración" sortable>
            <template #body="slotProps">
              <span class="flex items-center gap-x-2">
                <Rating
                  :modelValue="slotProps.data.rating"
                  :readonly="true"
                  :cancel="false"
                  :cancelTooltip="false"
                />
                <span class="text-xs text-slate-400">
                  ({{ slotProps.data.reviews }})
                </span>
              </span>
            </template>
          </Column>
          <Column field="contact_person" header="Contacto"></Column>
        </DataTable>
      </div>
    </transition>
  </div>
</template>
<script setup>
import { ref, computed, shallowRef } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useToast } from "primevue/usetoast";
import { useUserStore } from "/src/stores/useUserStore.js";
import Loading from "@/components/Loading.vue";
import Main from "/src/layouts/Main.vue";
import { PROVIDER_COLOR, PROVIDER_HEX } from "/src/constants/colors.js";
import { PROVIDER_LABEL } from "/src/constants/labels.js";
import AddNewProvider from "@/components/properties/AddNewProvider.vue";

import IconBolt from "@/components/icons/IconBolt.vue";
import IconDroplet from "@/components/icons/IconDroplet.vue";
import IconLockSquareRounded from "@/components/icons/IconLockSquareRounded.vue";
import IconWall from "@/components/icons/IconWall.vue";
import IconElevator from "@/components/icons/IconElevator.vue";
import IconWindow from "@/components/icons/IconWindow.vue";
import IconPlant from "@/components/icons/IconPlant.vue";
import IconApiApp from "@/components/icons/IconApiApp.vue";
import IconAntenna from "@/components/icons/IconAntenna.vue";
import IconShieldCheck from "@/components/icons/IconShieldCheck.vue";
import IconShieldStar from "@/components/icons/IconShieldStar.vue";
import IconScale from "@/components/icons/IconScale.vue";
import IconPaint from "@/components/icons/IconPaint.vue";
import IconBucketDroplet from "@/components/icons/IconBucketDroplet.vue";
import IconStarFill from "@/components/icons/IconStarFill.vue";

defineOptions({
  name: "Providers",
  layout: Main,
});

const PROVIDER_ICONS = {
  electricity: IconBolt,
  plumbing: IconDroplet,
  locksmiths: IconLockSquareRounded,
  painters: IconPaint,
  antenna_technicians: IconAntenna,
  bricklayers: IconWall,
  elevators: IconElevator,
  glaziers: IconWindow,
  cleaning: IconBucketDroplet,
  gardening: IconPlant,
  security: IconShieldStar,
  insurance: IconShieldCheck,
  lawyers: IconScale,
  others: IconApiApp,
};

const loading = ref(false);

// utils
const http = useHttp();
const toast = useToast();
const user = useUserStore();

// variables
const search = ref("");
const providers = ref([]);
const providersLoading = ref(false);

const getProviders = async () => {
  providersLoading.value = true;
  try {
    const response = await http.get(`/suppliers/`);
    providers.value = response.data;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: error,
      life: 3000,
    });
  }
  providersLoading.value = false;
};

getProviders();

function updateItems() {
  setTimeout(() => {
    getProviders();
  }, 300);
}
const getTopRatedProviders = computed(() => {
  return providers.value
    .map((provider) => ({
      ...provider,
      weighted_score: provider.rating * Math.log10(provider.reviews + 1), // Ponderación por número de reviews
    }))
    .sort((a, b) => b.weighted_score - a.weighted_score) // Ordenar de mayor a menor
    .slice(0, 3);
});

const getWorstRatedProviders = computed(() => {
  return providers.value
    .map((provider) => ({
      ...provider,
      weighted_score: provider.rating * Math.log10(provider.reviews + 1), // Ponderación por número de reviews
    }))
    .sort((a, b) => a.weighted_score - b.weighted_score) // Ordenar de menor a mayor
    .slice(0, 3);
});

const getRatingDistribution = computed(() => {
  const total = providers.value.length;
  if (total === 0) return [];
  const distribution = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
  providers.value.forEach((provider) => {
    distribution[provider.rating]++;
  });

  const items = Object.keys(distribution).map((key) => ({
    rating: parseInt(key),
    value: ((distribution[key] / total) * 100).toFixed(0),
  }));

  return items.reverse();
});

const providerStats = computed(() => {
  const total = providers.value.length;
  if (total === 0) return [];
  const typeCounts = {};

  // Contar ocurrencias de cada type
  providers.value.forEach(({ type }) => {
    typeCounts[type] = (typeCounts[type] || 0) + 1;
  });

  // Convertir a array con porcentajes
  const stats = Object.entries(typeCounts).map(([type, count]) => ({
    label: PROVIDER_LABEL[type],
    color: PROVIDER_HEX[type] || "#000000",
    value: (count / total) * 100,
  }));

  // Ajustar porcentajes para que sumen 100%
  const sum = stats.reduce((acc, curr) => acc + curr.value, 0);
  const adjustmentFactor = 100 / sum;

  // Calcular valores ajustados pero sin redondear
  const adjustedStats = stats.map((stat) => ({
    ...stat,
    value: stat.value * adjustmentFactor,
  }));

  // Redondear hacia abajo y guardar los decimales restantes
  let remaining = 100;
  const finalStats = adjustedStats.map((stat) => {
    const floorValue = Math.floor(stat.value);
    remaining -= floorValue;
    return {
      ...stat,
      value: floorValue,
      decimal: stat.value - floorValue,
    };
  });

  // Distribuir el restante a los valores con mayores decimales
  while (remaining > 0) {
    const maxDecimalStat = finalStats.reduce(
      (max, curr) => (curr.decimal > max.decimal ? curr : max),
      finalStats[0]
    );
    maxDecimalStat.value += 1;
    maxDecimalStat.decimal = 0;
    remaining -= 1;
  }

  return finalStats.map(({ decimal, ...stat }) => stat);
});
</script>
