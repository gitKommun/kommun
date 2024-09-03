<template>
    <div :class="`min-w-56 p-3 max-w-64 flex flex-col rounded-xl min-h-56  bg-${priorityColor[incidence.priority]}-50 text-${priorityColor[incidence.priority]}-500`">
        <div class="flex justify-between items-center mb-1">
            <div :class="`h-8 w-8 rounded-lg flex items-center justify-center bg-${priorityColor[incidence.priority]}-100 text-${priorityColor[incidence.priority]}-500`">
                <IconFlag/>
            </div>
            <span class="text-xs">17/12/2024 18:32</span>
        </div>
        <div class="font-semibold mb-3 flex flex-1 min-h-0">{{ incidence.title }}</div>
        <div class="mt-auto">
            <div class="text-sm flex flex-col"><span :class="`text-xs text-${priorityColor[incidence.priority]}-300`">LUGAR:</span> <span>Ascensor</span></div>
            <div class="text-sm flex flex-col"><span :class="`text-xs text-${priorityColor[incidence.priority]}-300`">CATEGORIA:</span> <span>{{incidence.category}}</span></div>
        </div>
        
    </div>
</template>
<script setup>
import IconFlag from '/src/components/icons/IconFlag.vue'
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
    medium: 'yellow',
    high: 'orange',
    urgent:'red'
}
</script>