<template>
    <div class="flex flex-col rounded-lg p-4 bg-slate-50 gap-y-2">
        <span>
            <CustomTag :color="usageTagColor(property.usage)">
                  {{ property.usage }}
                </CustomTag>
        </span>
         
      <div class="">{{ property.address_complete }}</div> 
      <div class="flex gap-x-4 border-t border-slate-200 pt-3">
        <span class="text-sm text-slate-900"> <span class="uppercase text-slate-500 text-xs">Superficie:</span> {{ property.surface_area }} m<sup>2</sup></span>
        <span class="text-sm text-slate-900"> <span class="uppercase text-slate-500 text-xs">Participación:</span> {{ property.participation_coefficient }}</span>
        
      </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import CustomTag from "/src/components/CustomTag.vue";
import { USAGES } from "/src/constants/colors.js";

defineOptions({
    name: 'PropertyCard',
})

const props = defineProps({
    property: {
        type: Object,
        required: true
    }
})

const usageTagColor = (usage) => {
  return USAGES[usage];
};
</script>