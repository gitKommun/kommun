<template>
  <div class="">
    <Button
      severity="contrast"
      @click="showCreateIncidence = !showCreateIncidence"
      raised
    >
      <IconPlus />
      <span class="hidden md:flex">Nueva incidencia</span>
    </Button>
    <Dialog
      v-model:visible="showCreateIncidence"
      modal
      header="Nueva incidencia"
      class="w-120"
    >
      <div class="">
        <div class="mb-4">
          <InputText
            v-model="form.title"
            placeholder="Título"
            class="w-full"
            variant="filled"
          />
        </div>
        <div class="mb-3">
          <Textarea
            v-model="form.description"
            placeholder="Descripción"
            variant="filled"
            class="w-full"
          />
        </div>
        <div class="mb-4">
          <Select
            v-model="form.category"
            :options="categories"
            optionLabel="label"
            optionValue="value"
            placeholder="Categoría..."
            class="w-full"
            variant="filled"
          />
        </div>
        <div class="mb-4">
          <Select
            v-model="form.priority"
            :options="priorities"
            optionLabel="label"
            optionValue="value"
            placeholder="Prioridad"
            class="w-full "
            variant="filled"
          >
            <template #value="slotProps">
              <div v-if="slotProps.value" class="flex items-center">
                <span
                  :class="`flex text-${PRIORITY_COLOR[slotProps.value]}-500`"
                  ><IconFlag class="scale-75 mr-1" />
                  {{ priorityLabel[slotProps?.value] }}</span
                >
              </div>
              <span v-else>
                {{ slotProps.placeholder }}
              </span>
            </template>
            <template #option="slotProps">
              <span
                :class="`flex text-${
                  PRIORITY_COLOR[slotProps.option.value]
                }-500`"
                ><IconFlag class="scale-75 mr-1" /> {{ slotProps.option.label }}
              </span>
            </template>
          </Select>
        </div>
        <div class="mb-4">
            <ZoneSelector @update:selected="(zone) => form.zone = zone"/>
        </div>
      </div>
      <div class="flex justify-end gap-x-4 mt-4">
        <Button
          text
          severity="secondary"
          @click="showCreateIncidence = !showCreateIncidence"
          label="Cancelar"
        />
        <Button
          severity="contrast"
          @click="createIncidence"
          :loading="incidenceCreateLoading"
          label="Crear"
        />
      </div>
    </Dialog>
  </div>
</template>
<script setup>
import { ref, watch, computed } from "vue";
import IconPlus from "/src/components/icons/IconPlus.vue";
import IconFlag from "/src/components/icons/IconFlag.vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import CustomTag from "/src/components/CustomTag.vue";
import { PRIORITY_COLOR } from "/src/constants/colors.js";
import ZoneSelector from "/src/components/ZoneSelector.vue";

defineOptions({
  name: "AddNewOwner",
});
const getFormattedDate = () => {
  const today = new Date();
  const day = String(today.getDate()).padStart(2, "0");
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const year = String(today.getFullYear()).slice(-2);

  return `${day}/${month}/${year}`;
};
//variables
const showCreateIncidence = ref(false);
const incidenceCreateLoading = ref(false);
const form = ref({
  title: "",
  description: "",
  //user: '',
  priority: "",
  category: "low",
  status: "reported",
    incident_date: getFormattedDate,
    zone: null,
  //community_id:
});
const categories = ref([
  { label: "Mantenimiento", value: "maintenance" },
  { label: "Limpieza", value: "cleaning" },
  { label: "Seguridad", value: "security" },
]);

const priorities = ref([
  { label: "Baja", value: "low" },
  { label: "Media", value: "medium" },
  { label: "Alta", value: "high" },
  { label: "Urgente", value: "urgent" },
]);

const priorityLabel = {
  low: "Baja",
  medium: "Media",
  high: "Alta",
  urgent: "Urgente",
};

//instancia API
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

const emit = defineEmits(["update:owners"]);

const createIncidence = async () => {
  incidenceCreateLoading.value = true;
  console.log(user?.current_community?.community_id);
  if (validatedForm) {
    try {
      await http.post(
        `claims/${user?.current_community?.community_id}/create/`,
        form.value
      );
      toast.add({
        severity: "success",
        summary: "Ok",
        detail: "Has creado un nuevo propietario",
        life: 3000,
      });
      emit("update:items", true);
    } catch (error) {
      toast.add({
        severity: "error",
        summary: "Upps!! algo ha fallado",
        detail: error,
        life: 3000,
      });
    }
    showCreateIncidence.value = false;
    incidenceCreateLoading.value = false;
    form.value = {
      title: "",
      description: "",
      //user: '',
      priority: "",
      category: "",
      status: "reported",
      incident_date: null,
    };
  }
};

//utilities
const validatedForm = computed(() => {
  return (
    form.title.value.trim() !== "" &&
    form.description.value.trim() !== "" &&
    form.category.value.trim() !== "" &&
    form.priority.value.trim() !== ""
  );
});
</script>
