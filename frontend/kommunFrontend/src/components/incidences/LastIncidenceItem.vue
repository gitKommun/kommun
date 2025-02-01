<template>
    <div class="w-full p-3 flex flex-col rounded-2xl  border border-slate-200  bg-slate-50 overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-lg hover:bg-slate-50">
        <div class="flex justify-between items-center mb-3">
            <div :class="`h-8 w-8 rounded-xl flex items-center justify-center bg-white border border-slate-100 text-${priorityColor[incidence.priority]}-500`">
                <IconFlag class="scale-75"/>
            </div>
            <CustomTag :color="INCIDENCE_STATUS_COLOR[incidence.status]">{{ INCIDENCE_STATUS_LABEL[incidence.status] }}</CustomTag>
            
        </div>
        <div class="font-semibold mb-3 flex flex-col flex-1 min-h-0">
            
            {{ incidence.title }}
            <span class="text-xs text-slate-500 font-medium">{{ dateFormat(incidence.create_at) }}</span>
        </div>
        <div class="mt-auto flex border-t border-slate-200 py-1 gap-x-2">
            <div class="text-xs text-slate-500 flex">Ascensor,</div>
            <div class="text-xs text-slate-500 flex">{{incidence.category}}</div>
        </div>
        
    </div>
</template>
<script setup>
import IconFlag from '/src/components/icons/IconFlag.vue';
import CustomTag from '/src/components/CustomTag.vue';
import { PRIORITY_COLOR, INCIDENCE_STATUS_COLOR } from '/src/constants/colors.js';
import { INCIDENCE_STATUS_LABEL } from '/src/constants/labels.js';

defineOptions({
  name: 'LastIncidenceItem',
})

const props = defineProps({
        incidence: {
            type: Object,
        },
        
});

const priorityColor = {
    low: 'blue',
    medium: 'amber',
    high: 'orange',
    urgent:'red'
}

// const dateFormat = (itemDate) => {
//   const date = new Date(itemDate);
//   const day = String(date.getDate()).padStart(2, "0"); // Día con dos dígitos
//   const month = String(date.getMonth() + 1).padStart(2, "0"); // Mes con dos dígitos
//   const year = date.getFullYear(); // Año completo
//   return `${day}/${month}/${year}`;
// };
function dateFormat(dateString) {
  // Intenta crear un objeto Date directamente desde el string ISO
  const date = new Date(dateString);

  // Verifica si la fecha es válida
  if (isNaN(date.getTime())) {
    console.error("Fecha no válida:", dateString);
    return "Fecha no válida";
  }

  // Formatea la fecha como DD/MM/YYYY
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Los meses en JavaScript son 0-indexados
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}

</script>