<template>
  <Fieldset legend="Datos generales">
    <div class="py-4">
      <InputText
        v-model="form.name"
        placeholder="Nombre de la comunidad"
        class="w-full"
        variant="filled"
      />
    </div>
    <!-- <div class="py-4">
                <InputText 
                    v-model="form.address" 
                    placeholder="Dirección" 
                    class="w-full"
                    variant="filled"/>
            </div> -->
    <div class="py-4 flex gap-x-3">
      <Select
        v-model="form.province"
        :options="provinces"
        placeholder="Provincia"
        class="w-full"
        variant="filled"
      />
      <!-- <InputText 
                    v-model="form.province" 
                    placeholder="Provincia" 
                    class="w-full"
                    variant="filled"/> -->
      <InputText
        v-model="form.city"
        placeholder="Ciudad"
        class="w-full"
        variant="filled"
      />
    </div>
    <div class="py-4 flex gap-x-3">
      <InputText
        v-model="form.address"
        placeholder="Dirección"
        class="w-full"
        variant="filled"
      />
      <InputText
        v-model="form.postal_code"
        placeholder="Código postal"
        variant="filled"
      />
    </div>

    <div class="py-4 flex gap-x-3">
      <InputText
        v-model="form.catastral_ref"
        placeholder="Referencia Catastral"
        variant="filled"
      />
      <InputText v-model="form.cif" placeholder="CIF" variant="filled" />
    </div>
    <div class="w-full flex justify-end">
      {{ props.id }}
      <Button severity="contrast" size="small" @click="updateCommunity()">
        Guardar
      </Button>
    </div>
  </Fieldset>
</template>
<script setup>
import { ref, watch, reactive, onMounted, shallowReactive } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

defineOptions({
  name: "GeneralData",
});

const props = defineProps({
  community: {
    type: Object,
  },
});
//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

// //variables
const form = ref({
  name: props.community.name,
  address: props.community.address,
  city: props.community.city,
  postal_code: props.community.postal_code,
  cif: props.community.cif,
  province: props.community.province,
  image: "",
  catastral_ref: props.community.catastral_ref,
});

const provinces = ref([]);

const hasChanged = ref(false);

watch(form, (newValue) => {
  hasChanged.value = true;
  //console.log('cambiando')
});

watch(
  () => props.community,
  (newCommunity) => {
    form.value.name = props.community.name || "";
    form.value.address = props.community.address || "";
    form.value.city = props.community.city || "";
    form.value.postal_code = props.community.postal_code || "";
    // Puedes inicializar otros campos según sea necesario
  },
  { immediate: true } // Ejecutar el watcher inmediatamente
);

const updateCommunity = () => {
  console.log("object :>> ", props.community);
  try {
    const response = http.put(
      `communities/${props.community.community_id}/update/`,
      {
        //...form.value
        name: form.value.name,
        address: form.value.address,
        city: form.value.city,
        postal_code: form.value.postal_code,
      }
    );
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "Carpeta creada con exito",
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
};

onMounted(async () => {
  try {
    const response = await http.get(`core/provinces/`);
    provinces.value = response.data;
  } catch (error) {
    toast.add({
      severity: "danger",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
});

</script>
