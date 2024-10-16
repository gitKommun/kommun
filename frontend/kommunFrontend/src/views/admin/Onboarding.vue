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
                <div class="w-110 py-3 ">
                    <div class="text-slate-400 text-xs mb-2">Indica la referencia catastral de la parcela de tu comunidad o de los inmuebles y nos otros nos encargamos del resto. Si no la conoces puedes consultarla 
                        <a 
                        href="https://www1.sedecatastro.gob.es/Cartografia/mapa.aspx?buscar=S" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="text-blue-500 hover:text-blue-700 underline"
                        >Aqui</a>
                    </div>
                    <div v-for="(option, index) in form.catastral_refs" :key="index" class="flex items-center w-full gap-x-2 py-1 mb-2 relative">
                        <InputText 
                        v-model="form.catastral_refs[index]"  
                        placeholder="Ejem:8428904VK6892N" 
                        variant="filled"
                        class="w-full"/>
                        <Button 
                        severity="danger"
                        text 
                        class="min-w-10 absolute right-0 -mr-14"
                        v-if="index>0"
                        @click="removeOption(index)">
                            <IconTrash/>
                        </Button>
                    </div>
                    <Button 
                        text
                        @click="addOption()"
                        >
                        <IconPlus/>
                        Nueva referencia catastral
                    </Button>
                    
                </div>
                <div class="w-110  flex justify-center">
                    <Button severity="contrast" @click="start()" raised>
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
import { useRouter } from 'vue-router';
import IconTrash from '@/components/icons/IconTrash.vue';
import IconPlus from '@/components/icons/IconPlus.vue';


defineOptions({
  name: 'onboarding',

})

const form = ref({
    name: '',
    catastral_refs: ['']
    
})

const addOption = () => {
  form.value.catastral_refs.push('')
}

const removeOption = (index) => {
  if (form.value.catastral_refs.length > 1) {
    form.value.catastral_refs.splice(index, 1);
  }
};

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const router = useRouter();

const createCommunity = () => {
    try {
            http.post(`communities/create/`, {
            name: form.value.name !== ''? form.value.name : 'Comunidad sin nombre',
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
const createProperties = async () => {
    if (form.value.catastral_refs[0] !== '') {
        try {
            await http.post(`properties/${user?.current_community?.community_id}/load-properties-API/`, {
            ref_catastrales: [...form.value.catastral_refs],

            })
        } catch (error) {
            toast.add({
                severity: 'danger',
                summary: 'Upps!! algo ha fallado',
                detail: error,
                life: 3000
            });
        }
    }    
}
const start =  () => {
    createCommunity()
    createProperties()
    router.push({ name: 'owners' });
}

</script>
