<template>
    <div class="w-full bg-slate-50 rounded-lg p-3 mb-3">
        <span class="text-xs text-slate-500">{{ item.event_date }}</span>
        <!-- <span class="text-xs text-slate-500">{{ formatDateTime(item.event_date) }}</span> -->
        <p class="w-full flex flex-wrap">Cambio de estado de: <CustomTag :color="INCIDENCE_STATUS_COLOR[item.event_old_status]" class="mx-1">{{ INCIDENCE_STATUS_LABEL[item.event_old_status]}}</CustomTag>  a <CustomTag :color="INCIDENCE_STATUS_COLOR[item.event_new_status]" class="mx-1">{{ INCIDENCE_STATUS_LABEL[item.event_new_status]}}</CustomTag> </p>
    </div>
</template>
<script setup>
import { ref, watch, computed } from 'vue'
import CustomTag from '../CustomTag.vue';
import { formatDateTime } from "@/utils/dateUtils";
import {
  INCIDENCE_STATUS_COLOR
} from "/src/constants/colors.js";
import {
  INCIDENCE_STATUS_LABEL
} from "/src/constants/labels.js";
defineOptions({
    name: 'IncidenceTimelineStatus',
})
const props = defineProps({
    item: {
        type: Object,
    },
});
</script>