<template>
  <div
    class="flex flex-col rounded-xl border p-3 w-full transition-all duration-300"
    :class="
      slot.reservation ? 'border-red-200' : 'border-green-200 cursor-pointer'
    "
    @click="reserveSlot()"
  >
    <div class="flex justify-between items-center">
      <span
        class="test-slate-500"
        :class="{ 'line-through text-red-500': slot.reservation }"
        >{{ slot.slot_start }} -
        {{ slot.slot_end }}</span
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
import { useConfirm } from "primevue/useconfirm";

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
const confirm = useConfirm();
const emit = defineEmits(['update:reserve']);

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


const reserveSlot = () => {
    if (props.slot.reservation) {
    return;
  }
  emit('update:reserve', true);
}



function dateFormat(dateString) {
  // Intenta crear un objeto Date directamente desde el string ISO
  const date = new Date(dateString);
  console.log(date);
  // Verifica si la fecha es válida
  if (isNaN(date.getTime())) {
    console.error("Fecha no válida:", dateString);
    return "Fecha no válida";
  }

  // Formatea la fecha como DD/MM/YYYY
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Los meses en JavaScript son 0-indexados
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}

const comfirmReserve = () => {
  confirm.require({
    message: "vas a reservar "+props.zone.name+" de "+formatTime(props.slot.slot_start)+" a "+formatTime(props.slot.slot_end)+" el día"+dateFormat(props.slot.slot_start)+"\n¿ Quieres confirmar la reserva?",
    header: "Confirmación de reserva ",
    rejectProps: {
      label: "Cancelar",
      severity: "secondary",
      outlined: true,
    },
    acceptProps: {
      label: "Confirmar reserva",
      severity: "contrast",
    },
    accept: () => {
    //   http.delete(
    //     `common_areas/${props.zone.community_id}/${props.zone.area_id}/slots/${props.slot.slot_id}/`
    //   );
      toast.add({
        severity: "success",
        summary: "Ok",
        detail: props.zone.name+ " se reservado con exito",
        life: 3000,
      });
      emit("update:slots");
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Upps!!",
        detail: "No se han podido reservar "+props.zone.name,
        life: 3000,
      });
    },
  });
};

</script>
