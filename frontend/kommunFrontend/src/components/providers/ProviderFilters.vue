<template>
  <Dropdown strategy="fixed">
    <template #reference="{ open }">
      <Button size="small" severity="secondary" @click="open">
        <IconFilter />
      </Button>
    </template>
    <template #content="{ close }">
      <div class="w-64 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 ">
        <div class="">
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
        </div>
      </div>
    </template>
  </Dropdown>
</template>

<script setup>
import { ref } from "vue";
import Dropdown from "/src/components/Dropdown.vue";
import IconFilter from "/src/components/icons/IconFilter.vue";

defineOptions({
  name: "ProviderFilters",
});

const form = ref({
  type: null,
});
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
</script>
