<template>
  <div
    class="flex flex-col rounded-xl border p-3 w-full transition-all duration-300"
    :class="
      slot.reserved ? 'border-red-200' : 'border-green-200 cursor-pointer'
    "
    @click="reserveSlot()"
  >
    <div class="flex justify-between items-center">
      <span
        class="test-slate-500"
        :class="{ 'line-through text-red-500': slot.reserved }"
        >{{ formatTime(slot.slot_start) }} - {{ formatTime(slot.slot_end) }}</span
      >
      <CustomTag :color="color">{{
        slot.reserved ? "Reservado" : "Libre"
      }}</CustomTag>
    </div>
    <div v-if="slot.reserved" class="flex items-center gap-x-2 mt-2">
      <Chip :label="slot.neighbor.fullName" class="text-xs" />
      <IconTrash
        v-if="slot.neighbor.person_id === user.current_community.community_person_id"
        @click.stop="deleteReserve()"
        class="scale-75 ml-auto text-red-500"
      />
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import { formatTime } from "@/utils/dateUtils";

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
const emit = defineEmits(["update:reserve", "update:slots"]);

const color = computed(() => {
  return props.slot.reserved ? "red" : "green";
});


const reserveSlot = () => {
  if (props.slot.reserved) {
    return;
  }
  emit("update:reserve", true);
};


const deleteReserve = () => {
  confirm.require({
    message:
      "Anular reserva de " +
      props.zone.name +
      " de " +
      formatTime(props.slot.slot_start) +
      " a " +
      formatTime(props.slot.slot_end) +
      "\n ¿Quieres confirmar la anulación?",
    header: "Anulación de reserva ",
    rejectProps: {
      label: "Cancelar",
      severity: "secondary",
      outlined: true,
    },
    acceptProps: {
      label: "Anular reserva",
      severity: "contrast",
    },
    accept: async () => {
      try {
        await http.delete(
          `common_areas/${user.current_community.community_id}/${props.zone.area_id}/reservations/${props.slot.reservation_id}/delete/`
        );
        toast.add({
          severity: "success",
          summary: "Ok",
          detail: props.zone.name + " se ha anulado con éxito",
          life: 3000,
        });
        await emit("update:slots");
      } catch (error) {
        toast.add({
          severity: "error",
          summary: "Error",
          detail: "No se ha podido anular la reserva",
          life: 3000,
        });
      }
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Upps!!",
        detail: "No se han podido anular la reserva de " + props.zone.name,
        life: 3000,
      });
    },
  });
};

const updateSlots =  () => {
   emit("update:slots");
};
</script>
