<template>
  <div class="w-full">
    <p class="text-slate-500 text-xs">
      Carga de propiedades por referencia catastral.
    </p>
    <div class="flex gap-x-3 py-3 w-full md:w-1/2">
      <InputText
        v-model="reference"
        placeholder="Referencia catastral"
        class="w-full"
        size="small"
        variant="filled"
      />
      <Button 
        severity="contrast" 
        size="small" 
        @click="loadProperties()"
        :loading="apiLoading">
        <span v-if="apiLoading">Cargando</span>
        <span v-else>Cargar</span>
      </Button>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

defineOptions({
  name: "LoadProperties",
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

//emit
const emit = defineEmits(["update:loaded"]);

//variables
const reference = ref("");
const apiLoading = ref(false);

function loadProperties() {
  
    if (reference.value !== "") {
    apiLoading.value = true;
    createProperties();
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "Todas las propiedades se han creado con exito",
      life: 3000,
    });
  } else {
    toast.add({
      severity: "error",
      summary: "Upps!!",
      detail: "El campo de referencia catastral no puede estar vacio",
      life: 3000,
    });
  }
}

const createProperties = async () => {
  try {
    await http.post(
      `properties/${user?.current_community?.community_id}/load-properties-API/`,
      {
        //...form.value
        ref_catastrales: [reference.value],
      }
    );
    apiLoading.value = false;
    emit("update:loaded", true);
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
