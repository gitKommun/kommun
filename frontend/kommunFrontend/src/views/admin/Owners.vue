<template>
  <div class="flex-1 min-h-0 overflow-y-scroll relative">
    <transition
      enter-active-class="transition-all transition-slow ease-out overflow-hidden"
      leave-active-class="transition-all transition-slow ease-in overflow-hidden"
      enter-class="opacity-0"
      enter-to-class="opacity-100"
      leave-class="opacity-100"
      leave-to-class="opacity-0"
      mode="out-in"
    >
    </transition>
    <div
      v-if="loading"
      class="h-full w-full flex justify-center items-center"
      key="loading"
    >
      <Loading />
    </div>
    <div v-else class="h-full w-full flex flex-col pt-3 overflow-y-scroll" key="content">
      <div class="w-full p-4 flex justify-between">
        <InputText
          v-model="search"
          placeholder="Buscar"
          size="small"
          variant="filled"
        />
        <AddNewOwner @update:owners="updateOwners" class="h-auto" />
      </div>
      <div class="px-4">
        <DataTable
          :value="owners"
          paginator
          :rows="20"
          :rowsPerPageOptions="[20, 40, 60, 100]"
          tableStyle="min-width: 50rem"
          class="text-sm"
        >
          <Column field="name" header="Nombre">
            <template #body="slotProps">
              <CustomAvatar
                :name="slotProps.data.name + ' ' + slotProps.data.surnames"
              />
              <span class="ml-3">{{ slotProps.data.name }}</span>
              <span class="ml-1">{{ slotProps.data.surnames }}</span>
            </template>
          </Column>
          <Column field="email" header="Email"></Column>
          <Column header="Rol">
            <template #body="slotProps">
              <CustomTag :color="rolesTagColor(slotProps.data.roles[0])">
                {{ rolesTagLabel(slotProps.data.roles[0]) }}
              </CustomTag>
            </template>
          </Column>
          <Column
            :rowEditor="true"
            style="width: 10%; min-width: 8rem"
            bodyStyle="text-align:right"
          >
            <template #body="slotProps">
              <Dropdown strategy="fixed">
                <template #reference="{ open }">
                  <div
                    class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer"
                    @click="open"
                  >
                    <IconDotsHorizontal class="text-slate-500" />
                  </div>
                </template>
                <template #content="{ close }">
                  <div
                    class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm"
                  >
                    <div
                      class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
                      @click="openUpdateOwner(slotProps.data)"
                    >
                      <IconPencil class="scale-75" />
                      <span>Editar</span>
                    </div>
                    <div
                      class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                      @click="confirmDelete(slotProps.data.person_id)"
                    >
                      <IconTrash class="scale-75" />
                      <span>Eliminar</span>
                    </div>
                  </div>
                </template>
              </Dropdown>
            </template>
          </Column>
        </DataTable>
        <Dialog
          v-model:visible="showUpdateOwner"
          modal
          header="Actualizar propietario"
          class="w-96"
        >
          <div class="">
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
            <div class="mt-4">
              <Select
                v-model="form.roles[0]"
                :options="userTypes"
                optionLabel="label"
                optionValue="value"
                placeholder="Rol..."
                class="w-full mb-4"
                variant="filled"
              />
            </div>
          </div>
          <div class="flex justify-end gap-x-4">
            <Button
              text
              severity="secondary"
              @click="showUpdateOwner = !showUpdateOwner"
              label="Cancelar"
            />
            <Button
              severity="contrast"
              @click="updateOwner"
              :loading="ownerUpdateLoading"
              label="Actualizar"
            />
          </div>
        </Dialog>
        <ConfirmDialog></ConfirmDialog>
        <Toast />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, shallowRef, reactive, onMounted } from "vue";
import Main from "/src/layouts/Main.vue";
import AddNewOwner from "/src/components/owners/AddNewOwner.vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import IconDotsHorizontal from "/src/components/icons/IconDotsHorizontal.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";
import IconPencil from "/src/components/icons/IconPencil.vue";
import Dropdown from "/src/components/Dropdown.vue";
import { useToast } from "primevue/usetoast";
import CustomTag from "/src/components/CustomTag.vue";
import CustomAvatar from "/src/components/CustomAvatar.vue";
import { ROLES } from "/src/constants/colors.js";
import { useConfirm } from "primevue/useconfirm";
import Loading from "@/components/Loading.vue";

defineOptions({
  name: "members",
  layout: Main,
});

//variables
const search = ref("");
const owners = ref([]);
const form = ref({
  name: "",
  surname: "",
  email: "",
  password: "1234",
  roles: [],
});
const ownerUpdateLoading = ref(false);
const loading = ref(true);

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const confirm = useConfirm();

const rolesTagColor = (rol) => {
  return ROLES[rol];
};
const tagLabel = {
  admin: "Admin",
  owner: "Propietario",
  tenant: "Inquilino",
  temp: "Temporal",
};
const rolesTagLabel = (rol) => {
  return tagLabel[rol];
};
const userTypes = ref([
  { label: "Administrador", value: "admin" },
  { label: "Propietario", value: "owner" },
]);
const showUpdateOwner = ref(false);
//get owners

const getOwners = async () => {
  try {
    const response = await http.get(
      `communities/${user?.current_community?.community_id}/neighbors/`
    );
    owners.value = response.data;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
  loading.value = false;
};

getOwners();

//delete owner
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
      updateOwners();
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

//update owner

const openUpdateOwner = (item) => {
  showUpdateOwner.value = true;
  //falta ajustar campos
  form.value = item;
};
const updateOwner = async () => {
  try {
    await http.put(
      `communities/${user?.current_community?.community_id}/neighbors/${form.value.person_id}/update/`,
      form.value
    );
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

function updateOwners() {
  console.log("update");
  setTimeout(() => {
    getOwners();
  }, 300);
}
</script>
