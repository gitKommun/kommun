<template>
  <div
    class="flex flex-col rounded-xl border p-3 w-full transition-all duration-300"
    :class="
      slot.reservation ? 'border-red-200' : 'border-green-200 cursor-pointer'
    "
  >
    <div class="flex justify-between items-center">
      <span
        class="test-slate-500"
        :class="{ 'line-through text-red-500': slot.reservation }"
        >{{ formatTime(slot.slot_start) }} -
        {{ formatTime(slot.slot_end) }}</span
      >
      <CustomTag :color="color">{{
        slot.reservation ? "Reservado" : "Libre"
      }}</CustomTag>
    </div>
    <div v-if="slot.reservation" class="flex items-center gap-x-2 mt-2">
      <CustomAvatar :name="slot.user" size="small" />
      <span class="ml-2 text-xs text-slate-500">{{ slot.user }}</span>
      <IconTrash class="scale-75 ml-auto text-red-500" />
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import CustomTag from "/src/components/CustomTag.vue";
import CustomAvatar from "/src/components/CustomAvatar.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";

defineOptions({
  name: "SlotZone",
});
const props = defineProps({
  zone: {
    type: Object,
  },
  slot: {
    type: Object,
  },
});
//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

const color = computed(() => {
  return props.slot.reservation ? "red" : "green";
});

//miscelanea
const formatTime = (time) => {
  const date = new Date(time);
  return date.toLocaleTimeString("es-ES", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
};
</script>
