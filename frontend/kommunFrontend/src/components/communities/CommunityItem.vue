<template>
    <div class="flex flex-col min-h-80 items-center border border-slate-200 p-2 rounded-2xl gap-x-3 mb-3 w-full max-w-72 bg-slate-100  hover:shadow-lg hover:bg-slate-50 relative group cursor-pointer transition-all duration-300">
        <div class="h-24 w-full bg-slate-200 rounded-lg relative">
          
            <CustomTag
            v-if="isCurrent"
            class="absolute top-0 left-0 ml-2 mt-2 shadow-green-700"
            :solid="true"
            :color="'green'"
            >
            Actual
            </CustomTag>
        </div>
        <div class="py-2 flex w-full px-1 font-semibold">
            {{ community.nameCommunity }}
        </div>
        <div class="py-1 flex w-full px-1 text-sm text-slate-400">
            Calle del pez volador Nº2, Valencia, Valencia
        </div>

        <div class="py-1 flex w-full px-1 text-xs text-slate-400 uppercase ">
            Propiedades: <span class="ml-1">0</span>
        </div>
        <div class="py-1 flex w-full px-1 text-xs text-slate-400 uppercase ">
            Ref: <span class="ml-1">{{ community.IDcommunity }}</span>
        </div>
        <div class="py-1 mt-auto">
            <Button 
            v-if="!isCurrent"
            size="small"
            severity="contrast"
            outlined
            @click="setCurrent()"
            >
            Seleccionar
            </Button>
        </div>
    </div>
</template>
<script setup>
    import { ref, watch, computed} from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';

import CustomTag from '/src/components/CustomTag.vue'


    defineOptions({
        name: 'CommunityItem',
    })

    const props = defineProps({
        community: {
            type: Object,
        },
    });
    //utils
    const http = useHttp();
    const { user } = useUserStore();
    const toast = useToast();

    //emit
const emit = defineEmits(['update:community']);


//currentCommunity
const isCurrent = computed(()=> {
    return user?.current_community?.community_id === props.community.IDcommunity
})

const setCurrent = () => {
    try {
        const response = http.put(`members/me/update/`, {
            ...props.community
        })
        toast.add({
            severity: 'success',
            summary: 'OK',
            detail: 'Has cambiado de Comunidad',
            life: 3000
        });
       // window.location.reload();
    } catch (error) {
        toast.add({
            severity: 'danger',
            summary: 'Upps!! algo ha fallado',
            detail: error,
            life: 3000
        });
    }
}

    
</script>