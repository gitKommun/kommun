<template>
    <div v-if="hasInfo" class="flex flex-col min-h-80 items-center border border-slate-200 p-2 rounded-2xl gap-x-3 mb-3 w-full md:max-w-72 bg-slate-50 hover:shadow-lg hover:-translate-y-3 relative group transition-all duration-300">
        <div class="h-10 w-full flex items-start justify-between rounded-lg mb-3 pl-2">
          <IconCommunity class="text-indigo-500 scale-175 ml-4 mt-6"/>
            <CustomTag
            v-if="isCurrent"
            
            :solid="true"
            :color="'green'"
            >
            Actual
            </CustomTag>
        </div>
        <div class="py-2 flex w-full px-4 font-semibold mt-3">
            <span v-if="info.name">
                {{ info.name }}
            </span>
            <span v-else>Communidad sin nombre</span> 
        </div>
        <div class="py-2 flex w-full px-4 text-sm text-slate-400">
            <span v-if="info.address">
                {{ info.address }}
            </span>
            <span v-else>Sin dirrección</span> 
        </div>        
        <div class="py-1 flex w-full px-4 text-xs text-slate-400 uppercase ">
            <span v-if="info.properties">
                Propiedades: <span class="ml-1">{{ info.properties }}</span>
            </span>
            <span v-else>Sin propiedades</span>
        </div>
        <div  class="py-1 flex w-full px-4 text-xs text-slate-400 uppercase ">
            <span v-if="info.catastral_ref">
                Ref: <span class="ml-1">{{ info.catastral_ref }}</span>
            </span>
            <span v-else>Sin referecia catastral</span>
        </div>
        <div class="py-1 flex w-full px-4 text-xs text-slate-400 uppercase ">
            <span v-if=" info.profiles">
                Vecinos: <span class="ml-1">{{ info.profiles }}</span>
            </span>
            <span v-else>Sin vecinos</span>
            
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
import IconCommunity from '/src/components/icons/IconCommunity.vue'




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


const info = ref({});

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
async function getInfo () {
    try {
        const response =await http.get(`communities/${props.community.community_id}/`);
        info.value = response.data;

    } catch (error) {
        toast.add({
            severity: 'danger',
            summary: 'Upps!! algo ha fallado',
            detail: error,
            life: 3000
        });
    }
}

getInfo();
const configCommunity = () => {
    route.push({ name: 'community_settings', params: { id:props.community.community_id } })
}

const hasInfo = computed(()=> {
    return Object.keys(info).length > 0
})

    
</script>