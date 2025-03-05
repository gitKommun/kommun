<template>
  <div class="flex flex-col rounded-lg p-4 bg-slate-50 gap-y-2">
    <span class="flex gap-x-2" s>
      <CustomTag :color="usageTagColor(property.usage)">
        {{ property.usage }}
      </CustomTag>
    </span>

    <div class="">{{ property.address_complete }}</div>
    <div class="flex gap-x-4 border-t border-slate-200 pt-3">
      <span class="text-sm text-slate-900">
        <span class="uppercase text-slate-500 text-xs">Superficie:</span>
        {{ property.surface_area }} m<sup>2</sup></span
      >
      <span class="text-sm text-slate-900">
        <span class="uppercase text-slate-500 text-xs">Participación:</span>
        {{ property.participation_coefficient }}</span
      >
    </div>
    <div class="">
      <AddNewTenant @update:owners="assignTenant()" />
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import CustomTag from "/src/components/CustomTag.vue";
import { USAGES } from "/src/constants/colors.js";
import IconPlus from "/src/components/icons/IconPlus.vue";
import AddNewTenant from "/src/components/owners/AddNewTenant.vue";

defineOptions({
  name: "PropertyCard",
});

const props = defineProps({
  property: {
    type: Object,
    required: true,
  },
});

const usageTagColor = (usage) => {
  return USAGES[usage];
};

const assignTenant = async () => {

  try {
    await http.post(
      `properties/${user?.current_community?.community_id}/add-tenant-to-property/`,
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
