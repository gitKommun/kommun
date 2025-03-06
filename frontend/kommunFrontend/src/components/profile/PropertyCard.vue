<template>
  <div class="flex flex-col rounded-lg p-4 bg-slate-50 gap-y-2">
    <span class="flex gap-x-2" s>
      <CustomTag :color="usageTagColor(property.usage)">
        {{ property.usage }}
      </CustomTag>
    </span>

    <div class="">{{ property.address_complete }}</div>
    <div class="flex gap-x-4 pt-3">
      <span class="text-sm text-slate-900">
        <span class="uppercase text-slate-500 text-xs">Superficie:</span>
        {{ property.surface_area }} m<sup>2</sup></span
      >
      <span class="text-sm text-slate-900">
        <span class="uppercase text-slate-500 text-xs">Participación:</span>
        {{ property.participation_coefficient }}</span
      >
    </div>
    <div class="border-t border-slate-200 pt-3">
      <div v-if="property.tenant.length" class=" flex flex-col gap-y-2 mb-3 ">
         <span class="uppercase text-slate-500 text-xs">Inquilinos actuales</span>
         <AssignedTenant v-for="tenant in property.tenant" :key="tenant.id" :tenant="tenant" @update:tenants="updateTenants()"/>
      </div>
      <AddNewTenant @update:tenants="updateTenants()" :propertyId="property.property_id" />
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import CustomTag from "/src/components/CustomTag.vue";
import { USAGES } from "/src/constants/colors.js";
import IconPlus from "/src/components/icons/IconPlus.vue";
import AddNewTenant from "/src/components/owners/AddNewTenant.vue";
import AssignedTenant from "/src/components/profile/AssignedTenant.vue";

defineOptions({
  name: "PropertyCard",
});

const emit = defineEmits(["update:tenants"]);

const props = defineProps({
  property: {
    type: Object,
    required: true,
  },
});

const usageTagColor = (usage) => {
  return USAGES[usage];
};

const updateTenants = () => {
  emit("update:tenants", true);
};
</script>
