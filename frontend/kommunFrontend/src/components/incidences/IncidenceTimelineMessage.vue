<template>
    <div class="w-full bg-slate-50 rounded-lg p-3 mb-3">
        <span class="text-xs text-slate-500">{{ item.event_date }}</span>
        <!-- <span class="text-xs text-slate-500">{{ formatDateTime(item.event_date) }}</span> -->
        <p class="w-full flex flex-wrap">{{ item.event_text }}</p>
        <div class="mt-2">
            <CustomAvatar :name="item.event_user.name" size="small"/>
            <span class="ml-2 text-xs text-slate-500">{{ item.event_user.name }}</span>
        </div>
    </div>
</template>
<script setup>
import { ref, watch, computed } from 'vue'
import CustomAvatar from '/src/components/CustomAvatar.vue'
import { formatDateTime } from "@/utils/dateUtils";

defineOptions({
    name: 'IncidenceTimelineMessage',
})
const props = defineProps({
    item: {
        type: Object,
    },
});
</script>