<template>
    <div class="h-screen w-screen bg-slate-100  flex justify-center items-center p-4">
        <div class="w-full h-full bg-white rounded-2xl shadow-2xl p-3 overflow-y-scroll">
            <div class="flex items-center justify-center w-full pt-16 pb-8">
                <img alt="Kommun logo" class="h-48" src="@/assets/construcction.svg"  />
            </div>
            <div class="font-bold text-3xl w-full flex justify-center mb-3">
                ¡Vamos a construir tu primera comunidad!
            </div>
            <div class="flex flex-col items-center justify-center w-full">
                <div class="w-110 py-3">
                    <InputText  v-model="form.name" placeholder="Nombre de la comunidad" class="w-full" variant="filled"/>
                </div>
                <div class="w-110 py-3 flex flex-col">
                    <span class="text-sm mb-2"> Importar datos de los inmuebles por referencia catastral:</span>
                    <div class="flex gap-x-3">
                        <div class="w-full flex flex-col items-center justify-center h-32 rounded-xl bg-slate-100 border cursor-pointer hover:shadow-xl transition-all duration-300"
                            :class="catastral_import_mode==='global'?'border-purple-500 shadow-lg':'border-slate-200'"
                            @click="catastral_import_mode='global'"    
                        >
                            <IconCloudDownload class="mb-2" :class="catastral_import_mode==='global'?'text-purple-500':'text-slate-400'"/>
                            <span class="text-center text-sm">Global <br> <span class="text-xs text-slate-400">(por parcela)</span></span>
                        </div>
                        <div class="w-full flex flex-col items-center justify-center h-32 rounded-xl bg-slate-100 border cursor-pointer hover:shadow-xl transition-all duration-300"
                            :class="catastral_import_mode==='list'?'border-purple-500 shadow-lg':'border-slate-200'"
                            @click="catastral_import_mode='list'"    
                        >
                            <IconBuilding class="mb-2" :class="catastral_import_mode==='list'?'text-purple-500':'text-slate-400'"/>
                            <span class="text-center text-sm">Por Inmuebles <br> <span class="text-xs text-slate-400">(Plantilla de referencias)</span></span>
                        </div>
                    </div>  
                </div>
                <div class="w-110 py-3 ">
                    <transition-group
                    enter-active-class="transition-all transition-slow ease-in-out "
                    leave-active-class="absolute hidden transition-all transition-slow ease-in-out"
                    enter-from-class="opacity-0 translate-y-12"
                    enter-to-class="opacity-100 mt-0"
                    leave-class="opacity-100 mt-0"
                    leave-to-class="opacity-0 mt-6"
                    
                    >
                        <div v-if="catastral_import_mode==='global'" class="w-110 py-3" key="global_ref">
                            <InputText  v-model="form.catastral_ref" placeholder="Referencia de Parcela" class="w-full" variant="filled"/>
                        </div>
                        <div v-if="catastral_import_mode==='list'" class="w-110 py-3" key="list_ref">
                            <InputFileDraggable @update:files="updateFiles"/>
                        </div>
                    
                    </transition-group>
                    
                </div>
                <div class="w-110  flex justify-center">
                    <Button severity="contrast" @click="updateCommunity()" raised>
                        Comenzar
                    </Button>
                </div>
                
                
            </div>

        
        </div>
 
    </div>

</template>
<script setup>
import { ref } from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';

import IconBuilding from '@/components/icons/IconBuilding.vue';
import IconCloudDownload from '@/components/icons/IconCloudDownload.vue';
import InputFileDraggable from '/src/components/InputFileDraggable.vue';


defineOptions({
  name: 'onboarding',

})

const form = ref({
    name: '',
    catastral_ref:''
})

const catastral_import_mode = ref('')

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

const updateCommunity = () => {
    try {
        const response = http.put(`communities/${user?.current_community?.community_id}/update/`, {
            //...form.value
            nameCommunity: form.value.name,

        })
        toast.add({
            severity: 'success',
            summary: 'Ok',
            detail: 'Carpeta creada con exito',
            life: 3000
        });

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
