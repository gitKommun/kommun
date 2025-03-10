<template>
  <div
    class="flex items-center justify-between gap-x-2 border border-slate-200 rounded-lg px-2 py-1"
  >
    <div class="">
      <CustomAvatar :name="tenant.fullname" class="scale-75" />
      <span class="text-sm text-slate-900 ml-1">
        {{ tenant.fullname }}
      </span>
    </div>
    <Dropdown strategy="fixed">
      <template #reference="{ open }">
        <div
          class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer"
          @click="open"
        >
          <IconDots class="text-slate-500" />
        </div>
      </template>
      <template #content="{ close }">
        <div class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm">
          <div
            class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
            @click="showEditTenant = true"
          >
            <IconPencil class="scale-75" />
            <span>Editar</span>
          </div>
          <div
            class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
            @click="confirmDelete(tenant.person_id)"
          >
            <IconTrash class="scale-75" />
            <span>Eliminar</span>
          </div>
        </div>
      </template>
    </Dropdown>
    <Dialog
      v-model:visible="showEditTenant"
      modal
      header="Actualizar propietario"
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
          @click="showEditTenant = !showEditTenant"
          label="Cancelar"
        />
        <Button severity="contrast" @click="updateTenant" label="Actualizar" />
      </div>
    </Dialog>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";

import CustomAvatar from "/src/components/CustomAvatar.vue";
import IconDots from "/src/components/icons/IconDots.vue";
import IconPencil from "/src/components/icons/IconPencil.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";
import Dropdown from "/src/components/Dropdown.vue";
defineOptions({
  name: "AssignedTenant",
});
const props = defineProps({
  tenant: {
    type: Object,
    required: true,
  },
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const confirm = useConfirm();
const emit = defineEmits(["update:tenants"]);

//variables
const form = ref({
  name: props.tenant.name,
  surnames: props.tenant.surnames,
  email: props.tenant.email,
  roles: props.tenant.roles,
});
const showEditTenant = ref(false);

const updateTenant = async () => {
  try {
    await http.put(
      `communities/${user?.current_community?.community_id}/neighbors/${props.tenant.person_id}/update/`,
      form.value
    );
    emit("update:tenants", true);
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
  showEditTenant.value = false;
};



const confirmDelete = (id) => {
  confirm.require({
    message:
      "Esta acción no se puede revertir, ¿ Estas seguro de borrar este usuario?",
    header: "Confirmación",
    rejectProps: {
      label: "Cancel",
      severity: "secondary",
      outlined: true,
    },
    acceptProps: {
      label: "Borrar",
      severity: "danger",
    },
    accept: () => {
      http.delete(
        `communities/${user?.current_community?.community_id}/neighbors/${id}/delete/`
      );
      emit("update:tenants", true);
      toast.add({
        severity: "success",
        summary: "Ok",
        detail: "El usuario se ha eliminado con exito",
        life: 3000,
      });
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Upps!!",
        detail: "No se ha podido eliminar el usuario",
        life: 3000,
      });
    },
  });
};
</script>
