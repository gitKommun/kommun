<template>
    <div class="w-full bg-slate-50 rounded-lg p-3 mb-3">
        <span class="text-xs text-slate-500">{{ item.event_date }}</span>
        <!-- <span class="text-xs text-slate-500">{{ formatDateTime(item.event_date) }}</span> -->
        <p class="text-xs text-indigo-500 mt-1">Proveedor asignado</p>
        <p class="w-full flex flex-wrap">{{ item.event_company }}</p>
        <div class="w-full flex flex-col mt-2">    
            <span class="flex items-center ml-2 text-xs text-slate-500">
                <IconMobile class="scale-75 mr-1 text-indigo-500"/>
                {{ item.event_contact.phone }}
            </span>
            <span class="flex items-center ml-2 text-xs text-slate-500">
                <IconMail class="scale-75 mr-1 text-indigo-500"/>
                {{ item.event_contact.email }}
            </span>
        </div>
    </div>
</template>
<script setup>
import { ref, watch, computed } from 'vue'
import IconMobile from '@/components/icons/IconMobile.vue';
import IconMail from '@/components/icons/IconMail.vue';
import { formatDateTime } from "@/utils/dateUtils";

defineOptions({
    name: 'IncidenceTimelineContact',
})
const props = defineProps({
    item: {
        type: Object,
    },
});
</script>