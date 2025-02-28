<template>
  <div class="w-full">
    <Select
      v-model="selected"
      :options="providers"
      optionLabel="company_name"
      optionValue="supplier_id"
      variant="filled"
      placeholder="Seleccionar proveedor"
      class="w-full"
      filter
    />
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";

defineOptions({
  name: "ProviderSelector",
});
const props = defineProps({
  provider: {
    type: Object,
  },
});
//utils
const http = useHttp();
const { user } = useUserStore();

//variables
const selected = ref(null);
const providers = ref([]);
const providersLoading = ref(false);
const emit = defineEmits(["update:selected"]);

watch(selected, (newValue) => {
  emit("update:selected", newValue);
});

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

onMounted(() => {
  getProviders();
});
</script>
