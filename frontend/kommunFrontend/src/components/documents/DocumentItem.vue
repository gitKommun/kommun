<template>
    <div class="flex flex-col items-center border border-slate-200 p-2 rounded-2xl gap-x-3 mb-3 w-full max-w-72  hover:shadow-lg hover:bg-slate-50 relative group cursor-pointer transition-all duration-300">
        <div class="bg-blue-300 h-32 w-full rounded-lg"></div>
        <div class="w-full flex justify-between  px-2 py-2">
            <div class="w-full flex text-sm pl-2">
               <span class="truncate">
                {{ document.name }} 
                </span> 
            </div>
            <div class="min-w-10 pl-2">
                <Dropdown strategy="fixed">
                    <template #reference="{ open }">
                        <div 
                            class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer "
                            @click.stop="open"
                        >
                            <IconDots class="text-slate-500"/>
                        </div>
                    </template>

                    <template #content="{ close }">
                        <div class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm">
                            <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                                @click="downloadFile()"
                            >
                                <IconDownload class="scale-75"/>
                                <span>Descargar</span>
                            </div>
                            <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                                @click="deleteFolder()"
                                >
                                <IconTrash class="scale-75"/>
                                <span>Eliminar</span>
                            </div>
                        </div>
                    </template>
                </Dropdown>
            </div>
        </div>

        
        
    </div>
</template>
<script setup>
import { ref, shallowRef, watch } from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';

import IconDots from "/src/components/icons/IconDots.vue"
import IconTrash from "/src/components/icons/IconTrash.vue"
import IconDownload from "/src/components/icons/IconDownload.vue"
import Dropdown from "/src/components/Dropdown.vue"


    // options
    defineOptions({
        name: 'DocumentItem',
    })

    const props = defineProps({
        document: {
            type: Object,
            
        },
    });
//utilities
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

//variables
//const downloadLoading = ref(false)

//Descarga doc
const downloadFile = () => {
    try {
        const response = http.get(`documents/${user?.current_community?.community_id}/d/${props.document.document_id}/download/`);
        toast.add({
            severity: 'success',
            summary: 'Ok', 
            detail: 'El documento se ha descargado con exito',
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