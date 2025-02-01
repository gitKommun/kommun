<template>
  <div class="w-full">
    <Select
      v-model="selected"
      :options="zones"
      optionLabel="name"
      variant="filled"
      placeholder="Seleccionar zona"
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
  name: "ZoneSelector",
});
const props = defineProps({
  zone: {
    type: Object,
  },
});
//utils
const http = useHttp();
const { user } = useUserStore();

//variables
const selected = ref(null);
const zones = ref([]);

const emit = defineEmits(["update:selected"]);

watch(selected, (newValue) => {
  emit("update:selected", newValue);
});

const getZones = async () => {
  try {
    const response = await http.get(
      `common_areas/${user?.current_community?.community_id}/`
    );
    zones.value = response.data;
  } catch (error) {
    console.log(error);
  }
};
getZones();

onMounted(() => {
  getZones();
});
</script>
