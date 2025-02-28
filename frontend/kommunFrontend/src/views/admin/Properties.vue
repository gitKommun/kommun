<template>
  <div class="flex-1 min-h-0">
    <transition
      enter-active-class="transition-all transition-slow ease-out overflow-hidden"
      leave-active-class="transition-all transition-slow ease-in overflow-hidden"
      enter-class="opacity-0"
      enter-to-class="opacity-100"
      leave-class="opacity-100"
      leave-to-class="opacity-0"
      mode="out-in"
    >
      <div
        v-if="loading"
        class="h-full w-full flex justify-center items-center"
        key="loading"
      >
        <Loading />
      </div>
      <div
        v-else
        class="h-full w-full flex flex-col pt-3 overflow-y-scroll relative"
        key="content"
      >
        <div class="px-3 mb-3">
          <PropertiesDetails
            :hasProperties="hasProperties"
            @update:properties="getProperties"
          />
        </div>
        <div class="px-4 min-h-0 flex-1" v-if="!properties.length">
          <div class="w-full flex flex-col items-center justify-center py-24">
            <EmptyTask class="scale-75" />
            <span
              class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300"
            >
              Actualmente no hay propiedades
            </span>
            <span class="text-sm text-slate-500 max-w-100 text-center"
              >Indica la referencia catastral de la propiedad que deseas cargar
              y apareceran automaticamente</span
            >
          </div>
        </div>
        <div v-else class="px-4 min-h-0 flex-1 ">
          <!-- scrollHeight="700px" scrollable -->
          <div class="flex justify-between items-center mb-3">
            <InputText
              v-model="search"
              placeholder="Buscar"
              size="small"
              variant="filled"
            />
            <AddNewOwner @update:owners="updateOwners" class="h-auto" />
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
                <div
                  class="w-56 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm"
                >
                  <p class="text-xs text-slate-500 mb-3">
                    Eliminar todas las propiedades
                  </p>
                  <Button
                    severity="danger"
                    size="small"
                    @click="deleteAll"
                    class="w-full"
                  >
                    Eliminar
                  </Button>
                </div>
              </template>
            </Dropdown>
          </div>
          <DataTable
            :value="properties"
            paginator
            :rows="20"
            :rowsPerPageOptions="[20, 40, 60, 100]"
            tableStyle="min-width: 50rem"
            class="text-xs "
          >
            <Column
              field="address_complete"
              sortable
              header="Dirección"
            ></Column>
            <Column field="surface_area" sortable header="Sup. m&sup2"></Column>
            <Column
              field="participation_coefficient"
              sortable
              header="Participación"
            ></Column>
            <Column field="usage" sortable header="Uso">
              <template #body="slotProps">
                <CustomTag :color="usageTagColor(slotProps.data.usage)">
                  {{ slotProps.data.usage }}
                </CustomTag>
              </template>
            </Column>
            <Column header="Propietario">
              <template #body="slotProps">
                <div
                  v-if="!slotProps.data.owner"
                  @click="openAddOwner(slotProps.data)"
                  class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer"
                >
                  <IconUserAdd class="text-slate-500" />
                </div>
                <div v-else class="text-underline" @click="openAddOwner(slotProps.data)">
                  {{ slotProps.data.owner.full_name }}
                </div>
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </transition>
    <Dialog
        v-model:visible="showAddOwner"
        modal
        header="Vincular propietario"
        class="w-96"
      >
        <div class="mb-4">
          <UserSelector @update:selected="(owner) => selectionOwner(owner)" />
        </div>
        <div class="flex justify-end gap-x-4">
          <Button
            text
            severity="secondary"
            @click="showAddOwner = !showAddOwner"
            label="Cancelar"
          />
          <Button
            severity="contrast"
            @click="updateOwner "
            label="Vincular"
          />
        </div>
      </Dialog>
    <toast />
    <ConfirmDialog />
  </div>
</template>
<script setup>
import { ref, computed, toRaw } from "vue";
import Main from "/src/layouts/Main.vue";
import IconDots from "/src/components/icons/IconDots.vue";
import IconUserAdd from "@/components/icons/IconUserAdd.vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import { useRouter } from "vue-router";
import { useConfirm } from "primevue/useconfirm";
import CustomTag from "/src/components/CustomTag.vue";
import UserSelector from "/src/components/UserSelector.vue";
import { USAGES } from "/src/constants/colors.js";
import PropertiesDetails from "/src/components/properties/PropertiesDetails.vue";
import EmptyTask from "/src/components/emptys/EmptyTask.vue";
import Dropdown from "/src/components/Dropdown.vue";
import Loading from "@/components/Loading.vue";



defineOptions({
  name: "properties",
  layout: Main,
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const confirm = useConfirm();

//variables
const properties = ref([]);
const loading = ref(true);
const search = ref("");
const showAddOwner = ref(false);
const form = ref({});
const selectedOwner = ref({})

const getProperties = async () => {
  try {
    const response = await http.get(
      `properties/${user?.current_community?.community_id}/`
    );
    properties.value = response.data;
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

getProperties();

// const updateOwner = (owner, data) => {
//   console.log("owner :>> ", owner, data);
//   const { person_id } = owner;
//   const { property_id } = data;

//   console.log("des", person_id, property_id);
//   try {
//     http.post(
//       `properties/${user?.current_community?.community_id}/property-relationship/create/`,
//       {
//         property_id: property_id,
//         person_id: person_id,
//         type: "owner",
//       }
//     );
//     toast.add({
//       severity: "success",
//       summary: "Ok",
//       detail: "Prpietario vinculado con exito",
//       life: 3000,
//     });
//   } catch (error) {
//     toast.add({
//       severity: "error",
//       summary: "Upps!! algo ha fallado",
//       detail: error,
//       life: 3000,
//     });
//   }
// };
// const getOwners = async () => {
//   try {
//     const response = await http.get(
//       `communities/${user?.current_community?.community_id}/neighbors/`
//     );
//     owners.value = response.data;
//   } catch (error) {
//     console.log(error);
//   }
// };

// onMounted(() => {
//   getOwners();
// });

//Borrar propiedades
const deleteAll = () => {
  confirm.require({
    message:
      "Esta acción no se puede revertir, ¿ Estas seguro de borrar todas las propiedades?",
    header: "Confirmación ",
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
      //llamada aborrar propiedades
      const response = http.delete(
        `properties/${user?.current_community?.community_id}/delete-properties/`
      );
      toast.add({
        severity: "info",
        summary: "Ok",
        detail: "Todas las propiedades se han eliminado con exito",
        life: 3000,
      });

      setTimeout(() => {
        getProperties();
      }, 300);
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Upps!!",
        detail: "No se han podido eliminar las propieddades",
        life: 3000,
      });
    },
  });
};

//miscelanea
const usageTagColor = (usage) => {
  return USAGES[usage];
};

//saber si las propiedades
const hasProperties = computed(() => {
  return (
    properties.value.length > 0 || Object.keys(properties.value).length > 0
  );
});

//añadir propietario
const openAddOwner = (item) => {
  showAddOwner.value = true;
  form.value = item;
};

const selectionOwner = (owner) => {
  selectedOwner.value = toRaw(owner);
};

const updateOwner = async () => {

  try {
    await http.post(
      `properties/${user?.current_community?.community_id}/property-relationship/create/`,
      {
        property_id: form.value.property_id,
        person_id: selectedOwner.value.person_id,
        type: 'owner', //no se pueden asignar admins ?
      }
    );
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "Prpietario vinculado con exito",
      life: 3000,
    });
    getProperties();
    showAddOwner.value = false;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
};


</script>
