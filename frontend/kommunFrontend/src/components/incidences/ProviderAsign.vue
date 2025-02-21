<template>
  <div class="">
    <div
      class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
      @click="showAddProvider = true"
    >
      <IconWorker class="scale-75" />
      <span>Asignar proveedor</span>
    </div>
    <Dialog
      v-model:visible="showAddProvider"
      modal
      header="Vincular propietario"
      class="w-96"
    >
      <div class="mb-4">
        <ProviderSelector
          @update:selected="(provider) => selectionProvider(provider)"
        />
      </div>
      <div class="flex justify-end gap-x-4">
        <Button
          text
          severity="secondary"
          @click="showAddProvider = !showAddProvider"
          label="Cancelar"
        />
        <Button severity="contrast" @click="updateOwner" label="Vincular" />
      </div>
    </Dialog>
  </div>
</template>
<script setup>
import { ref } from "vue";
import IconWorker from "/src/components/icons/IconWorker.vue";
import ProviderSelector from "@/components/ProviderSelector.vue";
defineOptions({
  name: "ProviderAsign",
});
const props = defineProps({
  incidence: {
    type: Object,
  },
});
const showAddProvider = ref(false);
const selectionProvider = (provider) => {
  console.log(provider);
};
</script>
