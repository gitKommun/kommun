<template>
    <Fieldset legend="Zonas comunes">
        <div class="flex items-center justify-between mb-3">
            <p class="text-slate-500 text-xs">Regitra tus zonas comunes como piscinas, gimnasio, pista de padel ...</p>
            <div class="flex-none" v-if="zones.length">
                <Button 
                    severity="contrast"
                    size="small"
                    @click="showCreateZoneModal= true"
                    outlined
                    >
                    <IconPlus class="scale-75"/>
                    Nuevo
                </Button>
            </div>      
        </div> 

        <template v-if="!zones.length">
            <div  class="w-full flex flex-col items-center justify-center py-16">
                <EmptyTask class="scale-75"/>
                <span class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300">
                    Actualmente no hay áreas comunes
                </span>
                <span class="text-sm text-slate-500 max-w-80 text-center mb-3">Aun no hay registrado ningún elemento como zona comun</span>
                <Button 
                    severity="contrast"
                    @click="showCreateZoneModal= true"
                    >
                    Crear primer elemento
                </Button>
            </div>
        </template>
        <template v-else>
            <DataTable :value="zones" tableStyle="min-width: 50rem">
                <Column field="name" header="Nombre"></Column>
                <Column  header="Uso">
                    <template #body="slotProps">
                        <Tag :severity="slotProps.data.reservable?'info':'success'"  :value="slotProps.data.reservable?'Reserva':'Libre'"/>     
                    </template>
                </Column>
                <Column header="Tiempo">
                    <template #body="slotProps">
                        {{ slotProps.data.reservation_duration }} {{ slotProps.data.time_unit }}
                    </template>
                </Column>
                <Column  :rowEditor="true" style="width: 10%; min-width: 8rem" bodyStyle="text-align:right">
                    <template #body="slotProps">
                        <Dropdown strategy="fixed">
                            <template #reference="{ open }">
                                <div 
                                    class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer "
                                    @click="open"
                                >
                                    <IconDotsHorizontal class="text-slate-500"/>
                                </div>
                            </template>
                            <template #content="{ close }">
                                <div class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm">
                                    <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                                        @click="openUpdateZone(slotProps.data)"
                                    >
                                        <IconPencil class="scale-75"/>
                                        <span>Editar</span>
                                    </div>
                                    <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                                        @click="deleteZone(slotProps.data.area_id)"
                                        >
                                        <IconTrash class="scale-75"/>
                                        <span>Eliminar</span>
                                    </div>
                                </div>
                            </template>
                        </Dropdown>
                    </template>    
                </Column>
            </DataTable>
        </template>
        <Dialog v-model:visible="showCreateZoneModal" modal header="Crear nueva zona" class="w-96">
 
            <div class="gap-y-2">
                <InputText 
                    v-model="zone.name" 
                    placeholder="Nombre de la zona" 
                    class="w-full" 
                    variant="filled"/>
                <div class="flex items-center mt-6">
                    <span class="min-w-10">
                        <ToggleSwitch v-model="zone.reservable" />
                    </span>
                    <span class="ml-3"> La zona que puede ser reservada por los propitarios </span>
                </div> 
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                >
                    <div class="mt-3 rounded-xl p-3 " v-if="zone.reservable">
                        <span class="text-slate-500 text-sm">Define la franja de tiempo para el uso de la zona:</span>
                        <div class="flex gap-x-3 py-3">
                            <InputGroup>
                                <InputNumber 
                                    v-model="zone.reservation_duration" 
                                    placeholder="Tiempo"
                                    variant="filled"
                                    inputClass="w-12 mr-1"/>
                                <Select 
                                    v-model="zone.time_unit" 
                                    :options="timePeriods" 
                                    optionLabel="label" 
                                    optionValue="value"
                                    variant="filled"
                                    placeholder="Selecciona..."/>
                            </InputGroup>
                        </div>
                    </div>
                </transition>
            </div>

                <div class="flex justify-end gap-x-4 pt-4">
                    <Button 
                        text
                        severity="secondary"
                        @click="showCreateZoneModal =! showCreateZoneModal"
                    >
                        Cancelar
                    </Button>
                    <Button 
                        severity="contrast"
                    @click="createZone"
                    >
                    Crear
                    </Button>
                </div>

        </Dialog>
        <Dialog v-model:visible="showUpdateZone" modal header="Editar zona" class="w-96">
            <div class="gap-y-2">
                <InputText 
                    v-model="zone.name" 
                    placeholder="Nombre de la zona" 
                    class="w-full" 
                    variant="filled"/>
                <div class="flex items-center mt-6">
                    <span class="min-w-10">
                        <ToggleSwitch v-model="zone.reservable" />
                    </span>
                    <span class="ml-3"> La zona tiene que ser reservada por los propitarios </span>
                </div> 
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                >
                    <div class="mt-3 rounded-xl p-3 " v-if="zone.reservable">
                        <span class="text-slate-500 text-sm">Define la franja de tiempo para el uso de la zona:</span>
                        <div class="flex gap-x-3 py-3">
                            <InputGroup>
                                <InputNumber 
                                    v-model="zone.reservation_duration" 
                                    placeholder="Tiempo" 
                                    inputClass="w-12 mr-1"
                                    variant="filled"/>
                                <Select 
                                    v-model="zone.time_unit" 
                                    :options="timePeriods" 
                                    optionLabel="label" 
                                    optionValue="value" 
                                    placeholder="Selecciona..."
                                    variant="filled"/>
                            </InputGroup>
                            
                        </div>
                    </div>
                </transition>
            </div>

                <div class="flex justify-end gap-x-4 pt-4">
                    <Button 
                    text
                    severity="secondary"
                    @click="!showUpdateZone"
                    >
                        Cancelar
                    </Button>
                    <Button 
                    severity="contrast"
                    @click="updateZone()"
                    >
                        Actualizar
                    </Button>
                </div>

        </Dialog>
    </Fieldset>

</template>
<script setup>
    import { ref, computed, onMounted } from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import EmptyTask from "/src/components/emptys/EmptyTask.vue";
import IconPlus from "/src/components/icons/IconPlus.vue";
    import IconTrash from "/src/components/icons/IconTrash.vue";
    import IconPencil from "/src/components/icons/IconPencil.vue";
    import IconDotsHorizontal from "/src/components/icons/IconDotsHorizontal.vue";
    import Dropdown from "/src/components/Dropdown.vue"
    import Loading from '/src/components/Loading.vue';
    import { useToast } from 'primevue/usetoast';
    //import Tag from "/src/components/Tag.vue"
    
    defineOptions({
        name: 'CommonZones'
    })
    const props = defineProps({
        community: {
            type: Object,
        },
    });

    //variables
    const showCreateZoneModal = ref(false)
    const zone = ref({
        name: '',
        reservable: false,
        reservation_duration: '',
        time_unit: '',
    })
    const timePeriods = ref([
        { label: 'Minutos', value: 'MIN' },
        { label: 'Horas', value: 'HOUR' },
        {label:'Día Completo',value:'DAY'}
    ])
    const zones = ref([]);
    const zonesLoading = ref(true);
    const zonesNameValidation = ref(true);
    //instancia API
    const http = useHttp();
    //user store
    const { user } = useUserStore();
      //use toast
    const toast = useToast();

    const showUpdateZone = ref(false);

    //getZones
    async function getZones() { 
        if (props.community.community_id) {
            try {

                const response = await http.get(`common_areas/${props.community.community_id}/`);
                zones.value = response.data
                zonesLoading.value = false;

            } catch (error) {
                toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
            }
        }     
    }
    getZones();

//createZone


    const createZone = () => {
        if (zone.name != '') {
            zonesNameValidation.value = true;
            try {
            const response = http.post(`common_areas/${props.community.community_id}/create/`, zone.value );
            
            toast.add({ severity: 'success', summary: 'Ok', detail: 'Zona creada con exito', life: 3000 });
            updateItems()
            
            } catch (error) {

               toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
            }
            zone.value = {
                    name: '',
                    reservable: false,
                    reservation_duration: '',
                    time_unit: '',
                }
            showCreateZoneModal.value = false;
        } else {
            zonesNameValidation.value=false
        }
        
  
    } 
    //editZone
const openUpdateZone = (item) => {
    showUpdateZone.value = true;
    zone.value = item 
    
} 
const updateZone = () => {
    try {
        const response = http.put(`common_areas/${props.community.community_id}/${zone.value.area_id}/`, zone.value);
        toast.add({ severity: 'success', summary: 'Ok', detail: 'La zona se ha actualizado con exito', life: 3000 });

        showUpdateZone.value = false;
        zone.value = {
            name: '',
            reservable: false,
            reservation_duration: '',
            time_unit: '',
        }

    } catch (error) {
        toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
     updateItems()
} 
        //deleteZone

const deleteZone = (id) => {

    console.log('deleteeeee')
    try {
        http.delete(`common_areas/${props.community.community_id}/${id}/`);
        toast.add({ severity: 'success', summary: 'Ok', detail: 'La zona se ha eliminado con exito', life: 3000 });

    } catch (error) {
         toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
        updateItems()
} 
function updateItems() {
  setTimeout(() => {
    getZones();
  }, 300);
}
onMounted(() => {
    updateItems()
});



</script>
