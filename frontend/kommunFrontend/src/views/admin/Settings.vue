<template>
  <div class="h-full w-full overflow-y-scroll">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">Comunidad "{{ community.nameCommunity }}"</span>
      </div>
    </div>
    <div class="flex justify-center px-3 pb-6">
      <div class="w-full max-w-4xl flex flex-col gap-y-3">
        <div class="">
            <router-link 
                to="/communities" 
              >
              <Button severity="contrast" text size="small">
                 <IconBack class="scale-75"/> Volver a comunidades 
              </Button>
    
            </router-link> 
        </div>
        <!-- DATOS GENERALES -->
          <GeneralData :community="community"/>
          <!-- DATOS GENERALES -->
          <!-- PROPIEDADES -->
          <Properties :community="community"/>
          <!-- PROPIEDADES -->
          <!-- ZONAS COMUNES -->
          <CommonZones :community="community"/>
          <!-- ZONAS COMUNES -->
          <!-- ELIMINAR COMUNIDAD -->
           <div class="w-full flex justify-between py-3">
            <div class="text-sm text-slate-400">Al eliminar está comunidad, tambien se eliminaran las propiedades, zonas comunes y usuarios vinculados con ella </div>
            <div class="flex-none">
              <Button
                @click="confirmDelete()"
                severity="danger" 
                outlined
                >Eliminar comunidad
              </Button>
            </div>
           </div>
           <ConfirmDialog></ConfirmDialog>
          <!-- ELIMINAR COMUNIDAD -->
      </div>
      
    </div>
  </div>  
</template>
<script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from "primevue/useconfirm";
  
  import Main from '/src/layouts/Main.vue';

  import CommonZones from '/src/components/settings/CommonZones.vue'
  import Properties from '/src/components/settings/Properties.vue'
import GeneralData from '/src/components/settings/GeneralData.vue'
  import IconBack from '/src/components/icons/IconBack.vue'

  defineOptions({
    name: 'Settings',
    layout: Main
  })
  //utils
    const http = useHttp();
    const { user } = useUserStore();
    const toast = useToast();
    const route = useRoute();
    const router = useRouter()
    const confirm = useConfirm();


  //variables
  const title = ref('Configuración')
  const community_id = ref(null);
  const community = ref({});
  onMounted(() => {
    const { id } = route.params
    community_id.value= id

  })

watch(community_id, (n) => {
  getCommunity()
})

const getCommunity = async() => {
    if (community_id.value) {
       try {
            const response = await http.get(`communities/${community_id.value}/`)
            community.value=response.data


        } catch (erro) {
            toast.add({
                severity: 'danger',
                summary: 'Upps!! algo ha fallado',
                detail: error,
                life: 3000
            });
        }
    }
    
}
getCommunity()
console.log(confirm);
const confirmDelete = () => {
    confirm.require({
        message: 'Esta acción no se puede revertir, ¿estas seguro de borrar esta comunidad?',
        header: 'Confirmación',
        rejectProps: {
            label: 'Cancel',
            severity: 'secondary',
            outlined: true
        },
        acceptProps: {
          label: 'Borrar',
          severity:'danger'
        },
        accept: () => {
          const response =  http.delete(`communities/${community_id.value}/delete/`)
          toast.add({
            severity: 'info',
            summary: 'Ok',
            detail: 'La comunidad se ha eliminado con exito',
            life: 3000
          });
          router.push({name:'communities'})
        },
        reject: () => {
          toast.add({
            severity: 'error',
            summary: 'Upps!!',
            detail: 'No se ha podido eliminar la comunidad',
            life: 3000
          });
        }
    });
};
</script>

