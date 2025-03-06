<template>
  <div class="">
    <div class="flex items-center justify-center gap-x-2 text-sm px-2 py-2 rounded-md bg-slate-100 cursor-pointer text-indigo-500 hover:bg-indigo-50 transition-all duration-300 hover:text-indigo-700"
     @click="showCreateTenant = !showCreateTenant">
      <IconUserAdd class="scale-75" />
      Añadir inquilino
    </div>
    <Dialog
      v-model:visible="showCreateTenant"
      modal
      header="Añadir inquilino"
      class="w-96"
    >
      <div class="mb-4">
        <div class="flex gap-x-3 mb-4">
          <InputText
            v-model="form.name"
            placeholder="Name"
            class="w-full"
            variant="filled"
          />
          <InputText
            v-model="form.surnames"
            placeholder="Surname"
            class="w-full"
            variant="filled"
          />
        </div>
        <InputText
          v-model="form.email"
          placeholder="E-mail"
          class="w-full"
          variant="filled"
        />
      </div>
      <div class="flex justify-end gap-x-4">
        <Button
          text
          severity="secondary"
          @click="showCreateTenant = !showCreateTenant"
          label="Cancelar"
        />
        <Button
          severity="contrast"
          @click="createTenant"
          :loading="ownerCreateLoading"
          label="Crear"
        />
      </div>
    </Dialog>
  </div>
</template>
<script setup>
import { ref, computed } from "vue";
import IconUserAdd from "/src/components/icons/IconUserAdd.vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

defineOptions({
  name: "AddNewTenant",
});

const props = defineProps({
  propertyId: {
    type: String,
    required: true,
  },
});

//variables
const showCreateTenant = ref(false);
const tenantCreateLoading = ref(false);
const form = ref({
  property_id: props.propertyId,
  name: "",
  surnames: "",
  email: "",
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const emit = defineEmits(["update:tenants"]);

const createTenant = async () => {

  tenantCreateLoading.value = true;
  if (validatedForm) {
    try {
      await http.post(
        `properties/${user?.current_community?.community_id}/add-tenant-to-property/`,
        form.value
      );
      toast.add({
        severity: "success",
        summary: "Ok",
        detail: "Has creado un nuevo inquilino",
        life: 3000,
      });
    } catch (error) {
      toast.add({
        severity: "danger",
        summary: "Upps!! algo ha fallado",
        detail: error,
        life: 3000,
      });
    }
    showCreateTenant.value = false;
    tenantCreateLoading.value = false;
    form.value = {
       property_id: props.propertyId,
  name: "",
  surnames: "",
  email: "",
    };
    emit("update:tenants", true);
  }
};
const validatedForm = computed(() => {
  return (
    form.name.value.trim() !== "" &&
    form.surnames.value.trim() !== "" &&
    form.email.value.trim() !== ""
  );
});
</script>
