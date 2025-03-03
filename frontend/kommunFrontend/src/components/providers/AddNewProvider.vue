<template>
  <div class="">
    <Button
      severity="contrast"
      raised
      size="small"
      @click="showAddProvider = !showAddProvider"
    >
      <IconPlus />
      <span class="hidden md:flex">Añadir proveedor</span>
    </Button>
    <Dialog
      v-model:visible="showAddProvider"
      header="Añadir proveedor"
      class="w-96"
      :modal="true"
    >
      <Stepper value="1" linear class="basis-[50rem]">
        <StepList>
          <Step value="1">Empresa</Step>
          <Step value="2">Contacto</Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <div class="flex flex-col gap-4">
              <InputText
                variant="filled"
                v-model="form.company_name"
                placeholder="Empresa"
              />
              <InputText
                variant="filled"
                v-model="form.cif_nif"
                placeholder="CIF/NIF"
              />
              <InputText
                variant="filled"
                v-model="form.address"
                placeholder="Dirección"
              />
              <Select
                v-model="form.type"
                :options="providerTypes"
                filter
                optionLabel="label"
                optionValue="value"
                placeholder="Tipo de proveedor"
                class="w-full"
                variant="filled"
              />
              <InputText
                variant="filled"
                v-model="form.phone"
                placeholder="Teléfono"
              />
              <InputText
                variant="filled"
                v-model="form.email"
                placeholder="Email"
              />
            </div>
            <div class="flex justify-end gap-x-4 pt-4">
              <Button
                severity="secondary"
                text
                @click="showAddProvider = !showAddProvider"
              >
                Cancelar
              </Button>
              <Button
                severity="contrast"
                outlined
                @click="activateCallback('2')"
              >
                Siguiente
              </Button>
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="2">
            <div class="flex flex-col gap-4">
              <InputText
                variant="filled"
                v-model="form.contact_person"
                placeholder="Persona de contacto"
              />
              <InputText
                variant="filled"
                v-model="form.contact_person_email"
                placeholder="Email de la persona de contacto"
              />
              <InputText
                variant="filled"
                v-model="form.contact_person_phone"
                placeholder="Teléfono de la persona de contacto"
              />
            </div>
            <div class="flex justify-end gap-x-4 mt-4">
              <Button
                text
                severity="secondary"
                @click="activateCallback('1')"
                label="Atras"
              />
              <Button
                severity="contrast"
                @click="createProvider"
                :loading="providerCreateLoading"
                label="Crear"
              />
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>
    </Dialog>
    <Toast />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useToast } from "primevue/usetoast";
import IconPlus from "/src/components/icons/IconPlus.vue";

defineOptions({
  name: "AddNewProvider",
});
//utils
const http = useHttp();
const toast = useToast();
const emit = defineEmits(["update:providers"]);

const showAddProvider = ref(false);
const providerTypes = ref([
  { label: "Abogados", value: "lawyers" },
  { label: "Albañiles", value: "bricklayers" },
  { label: "Antenistas", value: "antenna_technicians" },
  { label: "Ascensores", value: "elevators" },
  { label: "Cerrajeros", value: "locksmiths" },
  { label: "Cristaleros", value: "glaziers" },
  { label: "Electricidad", value: "electricity" },
  { label: "Fontaneria", value: "plumbing" },
  { label: "Jardineria", value: "gardening" },
  { label: "Limpieza", value: "cleaning" },
  { label: "Otros", value: "others" },
  { label: "Pintores", value: "painters" },
  { label: "Seguros", value: "insurance" },
  { label: "Vigilancia", value: "security" },
]);
const form = ref({
  company_name: "",
  phone: "",
  email: "",
  address: "",
  type: "",
  contact_person: "",
  contact_person_email: "",
  contact_person_phone: "",
  cif_nif: "",
});

const providerCreateLoading = ref(false);
// verificar que todos los campos están llenos
const validatedForm = computed(() => {
  return (
    form.value.company_name &&
    form.value.phone &&
    form.value.email &&
    form.value.address &&
    form.value.type &&
    form.value.contact_person &&
    form.value.contact_person_email &&
    form.value.contact_person_phone &&
    form.value.cif_nif
  );
});

const createProvider = async () => {
  if (!validatedForm.value) {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Todos los campos son requeridos",
      life: 3000,
    });
    return;
  }
  providerCreateLoading.value = true;

  try {
    await http.post(`/suppliers/create/`, form.value);
    toast.add({
      severity: "success",
      summary: "Proveedor creado",
      life: 3000,
    });
    emit("update:providers", true);
    form.value = {
      company_name: "",
      phone: "",
      email: "",
      address: "",
      type: "",
      contact_person: "",
      contact_person_email: "",
      contact_person_phone: "",
      cif_nif: "",
    };
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Error al crear el proveedor",
      detail: error,
      life: 3000,
    });
  } finally {
    providerCreateLoading.value = false;
  }
};
</script>
