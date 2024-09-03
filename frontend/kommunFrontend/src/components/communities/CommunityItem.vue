<template>
    <div class="flex flex-col min-h-80 items-center border border-slate-200 p-2 rounded-2xl gap-x-3 mb-3 w-full md:max-w-72 bg-slate-100  hover:shadow-lg hover:bg-slate-50 relative group transition-all duration-300">
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
            {{ community.community_name }}
        </div>
        <div class="py-1 flex w-full px-1 text-sm text-slate-400">
            {{ community.address }}, {{ community.city }}
        </div>

        <div class="py-1 flex w-full px-1 text-xs text-slate-400 uppercase ">
            Propiedades: <span class="ml-1">0</span>
        </div>
        <div class="py-1 flex w-full px-1 text-xs text-slate-400 uppercase ">
            Ref: <span class="ml-1">{{ community.community_id }}</span>
        </div>
        <div class="w-full py-1 mt-auto flex justify-between">
            <Button 
            v-if="!isCurrent"
            size="small"
            severity="contrast"
            outlined
            @click="setCurrent()"
            >
            Seleccionar
            </Button>
            <div 
                class="h-8 w-8 rounded-xl flex items-center justify-center hover:bg-slate-100 transition-all duration-300 group ml-auto"
                @click="configCommunity()"
                >
                <IconSettings class="text-slate-400 group-hover:text-slate-950"/>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { ref, watch, computed} from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';

import CustomTag from '/src/components/CustomTag.vue'
import IconSettings from '/src/components/icons/IconSettings.vue'
import IconTrash from '/src/components/icons/IconTrash.vue'


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
const route = useRouter();
    

    //emit
const emit = defineEmits(['update:community']);


//currentCommunity
const isCurrent = computed(()=> {
    return user?.current_community?.community_id === props.community.community_id
})

const setCurrent = () => {
    try {
        const response = http.put(`members/me/update/`, {
            current_community: props.community.community_id
        })
        toast.add({
            severity: 'success',
            summary: 'OK',
            detail: 'Has cambiado de Comunidad',
            life: 3000
        });
        emit('update:community',true)
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

const configCommunity = () => {
    route.push({ name: 'settings', params: { id:props.community.community_id } })
}

    
</script>