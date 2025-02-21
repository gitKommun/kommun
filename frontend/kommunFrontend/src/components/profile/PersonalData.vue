<template>
  <Fieldset legend="Datos personales">
    <div class="flex flex-col md:flex-row gap-x-3 py-2 md:py-4">
      <InputText
        v-model="form.name"
        placeholder="Nombre"
        class="w-full mb-4 md:mb-0"
        variant="filled"
      />
      <InputText
        v-model="form.surname"
        placeholder="Apellidos"
        class="w-full"
        variant="filled"
      />
    </div>
    <div class="flex flex-col md:flex-row gap-x-3 py-2 md:py-4">
      <InputText
        v-model="form.email"
        placeholder="E-mail"
        class="w-full mb-4 md:mb-0"
        variant="filled"
      />
      <InputText
        v-model="form.phone"
        placeholder="Teléfono"
        class="w-full"
        variant="filled"
      />
    </div>
    <div class="flex items-center py-4">
      <InputGroup>
        <Select
          v-model="form.identificationType"
          :options="documentType"
          optionLabel="label"
          class="max-w-40"
          optionValue="value"
          placeholder="Selecciona..."
          variant="filled"
        />
        <InputText
          v-model="form.identificationNumber"
          placeholder="Número de identificación"
          class="max-w-64"
          variant="filled"
        />
      </InputGroup>
    </div>
    <div class="flex items-center py-4">
      <span class="min-w-10">
        <ToggleSwitch v-model="form.allowSharing" />
      </span>
      <span class="ml-3">
        Permitir que los otros propietarios tengan acesso a tus datos de
        contacto
      </span>

    </div>
    <div class="flex items-center justify-end pt-4">
      <Button severity="contrast" size="small" :disabled="!hasChanges" @click="updateOwner"> Guardar </Button>
    </div>
    <Toast />
  </Fieldset>
  
</template>
<script setup>
import { ref, watch } from "vue";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useHttp } from "/src/composables/useHttp.js";
import { useToast } from "primevue/usetoast";

defineOptions({
  name: "PersonalData",
});

//utils
const http = useHttp();
const toast = useToast();
const { user } = useUserStore();

//variables
const form = ref({
  name: user.name,
  surname: user.surnames,
  email: user.email,
  phone: user.phoneNumber,
  identificationNumber: user.documentID ? user.documentID : "",
  identificationType: user.documentType ? user.documentType : "",
  allowSharing: user.contactIsPublic,
  roles: user.current_community.community_roles
});

const documentType = ref([
  { label: "DNI", value: "DNI" },
  { label: "NIE", value: "NIE" },
  { label: "Pasaporte", value: "passport" },
]);


const hasChanges = ref(false);

watch(form, () => {
  hasChanges.value = true;
}, { deep: true }); 

const updateOwner = async () => {
  try {
    await http.put(
      `members/me/update/`,
      form.value
    );
    toast.add({
      severity: "success",
      summary: "¡Datos actualizados correctamente!",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
  showUpdateOwner.value = false;
};


</script>
