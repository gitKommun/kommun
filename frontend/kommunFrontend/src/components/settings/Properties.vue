<template>

    <Fieldset legend="Propiedades">

            <div class="flex flex-col mb-3">
                <p class="text-slate-500 text-xs">Carga de propiedades por referencia catastral.</p>
                <div class="flex gap-x-3 py-3 w-full md:w-1/2">
                    <InputText 
                    v-model="reference" 
                    placeholder="Referencia catastral" 
                    class="w-full"
                    size="small"
                    variant="filled"/>
                     <Button 
                    severity="contrast"
                    size="small"
                    @click="loadProperties()"
                    :loading="propertiesCreationLoading"
                    :disabled="properties.length"
                    >
                        Cargar
                    </Button>
                </div>
            </div>
            <div v-if="properties.length" class="flex gap-x-3 mb-4">
                <div 
                v-for="prop in groupedData"
                :key="prop.key"
                class="w-full flex flex-col justify-center items-center bg-slate-100 rounded-xl p-3">
                    <span 
                    class="uppercase text-xs mb-2"
                    :class="`text-[${prop.color}]`">
                        {{ prop.label }}
                    </span>
                    <span class="font-bold text-lg">{{ prop.count }}</span>
                </div>
            </div>
            <div v-if="properties.length" class="w-full py-2 text-sm mb-4">
                <span class="text-xs text-slate-400 mb-2">Propiedades por superficie</span>
                <MeterGroup :value="groupedData" />
            </div>
            <div v-if="properties.length" class="w-full flex justify-end gap-x-3">
                <Button 
                    severity="danger"
                    size="small"
                    @click="deleteAll"
                    outlined
                    >
                        Eliminar propiedades
                </Button>
            </div>

            <Toast />
    </Fieldset>

</template>
<script setup>
    import { ref, computed } from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';
import { USAGES_HEX } from '/src/constants/colors.js';
    import { useConfirm } from "primevue/useconfirm";

    defineOptions({
        name: 'Properties'
    })
    const props = defineProps({
        community: {
            type: Object,
        },
    });

    

    //instancia API
const http = useHttp();
const { user } = useUserStore();
const confirm = useConfirm();
const toast = useToast();

//variables

const properties = ref([]);
const reference = ref('');
const propertiesCreationLoading = ref(false)

const getProperties = async () => {
  try {
      const response = await http.get(`properties/${user?.current_community?.community_id}/`);
      properties.value = response.data
      
    } catch (error) {
     toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
}

getProperties()


const groupedData = computed(() => {
  const usageCount = {};
  const usageArea = {};
  let totalSurfaceArea = 0;

  // Agrupar y sumar superficie total
  properties.value.forEach((property) => {
    const usage = property.usage;
    const surfaceArea = parseFloat(property.surface_area);

    if (!usageCount[usage]) {
      usageCount[usage] = 0;
      usageArea[usage] = 0;
    }

    usageCount[usage] += 1;
    usageArea[usage] += surfaceArea;
    totalSurfaceArea += surfaceArea;
  });

  // Formatear los resultados para la salida esperada
  return Object.keys(usageCount).map((key) => {
    return {
      label: key,
      color: key ==='ALMACEN-ESTACIONAMIENTO'? USAGES_HEX.ALMACEN_ESTACIONAMIENTO: USAGES_HEX[key] || '#000000', // Color por defecto si no está en el objeto
      value: ((usageArea[key] / totalSurfaceArea) * 100).toFixed(2), // Porcentaje basado en surface_area,
      count: usageCount[key]
    };
  });
});


//load


function loadProperties  () {

    propertiesCreationLoading.value = true
    if (reference.value !== '') {
            createProperties()
    } else {
        toast.add({
        severity: 'error',
        summary: 'Upps!!',
        detail: 'El campo de referencia catastral no puede estar vacio',
        life: 3000
        });
    propertiesCreationLoading.value = false
    }
    

}

const deleteAll = () => {
    confirm.require({
        message: 'Esta acción no se puede revertir, ¿ Estas seguro de borrar todas las propiedades?',
        header: 'Confirmación ',
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
            //llamada aborrar propiedades
          const response =  http.delete(`properties/${props.community.community_id}/delete-properties/`)
          toast.add({
            severity: 'info',
            summary: 'Ok',
            detail: 'Todas las propiedades se han eliminado con exito',
            life: 3000
          });
            setTimeout(() => {
                getProperties()
            }, 300);
          
         
        },
        reject: () => {
          toast.add({
            severity: 'error',
            summary: 'Upps!!',
            detail: 'No se han podido eliminar las propieddades',
            life: 3000
          });
        }
    });
};
const createProperties = async () => {
    
    try {
        const response = await http.post(`properties/${user?.current_community?.community_id}/load-properties-API/`, {
            //...form.value
            ref_catastrales: [reference.value],

        })
    } catch (error) {
        toast.add({
            severity: 'danger',
            summary: 'Upps!! algo ha fallado',
            detail: error,
            life: 3000
        });
    }
    getProperties()
    propertiesCreationLoading.value = false
}




</script>