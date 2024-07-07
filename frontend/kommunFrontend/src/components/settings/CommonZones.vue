<template>
    <div class="p-4 border border-slate-200 rounded-2xl ">
        <div class="flex justify-between">
            <div class="flex flex-col w-full">
                <h3 class="text-slate-950 text-xl font-bold">Zonas comunes</h3>
                <p class="text-slate-500">Regitra tus zonas comunes como piscinas, gimnasio, pista de padel ...</p>
            </div>
            <div class="flex-none">
                <vs-button 
                    color="dark" 
                    class="inline"
                    type="border"
                    size="small"
                    @click="showCreateZoneModal= true"
                    >
                    <IconPlus class="scale-75"/>
                    Nuevo
                </vs-button>
            </div>      
        </div>    
        <template v-if="!zones.length">
            <div  class="w-full flex flex-col items-center justify-center py-16">
                <EmptyTask class="scale-75"/>
                <span class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300">
                    Actualmente no hay áreas comunes
                </span>
                <span class="text-sm text-slate-500 max-w-80 text-center mb-3">Aun no hay registrado ningún elemento como zona comun</span>
                <vs-button 
                    color="dark" 
                    class="inline"
                    @click="showCreateZoneModal= true"
                    >
                    Crear primer elemento
                </vs-button>
            </div>
        </template>
        <template v-else>
            <vs-table class="mt-4">
                <template #thead>
                    <vs-tr>
                        <vs-th> Nombre </vs-th>
                        <vs-th> Reseva </vs-th>
                        <vs-th> tiempo </vs-th>
                        <vs-th class="max-w-12 pr-2"></vs-th>
                    </vs-tr>
                </template>
                <template #tbody>
                    <vs-tr v-for="zone in zones" :key="zone.id" :data="zone">
                        <vs-td>
                          {{ zone.name }}
                        </vs-td>
                        <vs-td>
                          {{ zone.limited }}
                        </vs-td>
                        <vs-td>
                          {{ zone.slotTime }} {{ zone.slotUnits }}
                        </vs-td>
                        <vs-td class="max-w-12 pr-2">
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
                                            @click="openUpdateZone(zone)"
                                        >
                                            <IconPencil class="scale-75"/>
                                            <span>Editar</span>
                                        </div>
                                        <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                                            @click="deleteZone(zone)"
                                            >
                                            <IconTrash class="scale-75"/>
                                            <span>Eliminar</span>
                                        </div>
                                    </div>
                                </template>
                            </Dropdown>
                        </vs-td>

                    </vs-tr>
                </template>
            </vs-table>
        </template>
        <vs-dialog v-model="showCreateZoneModal" overlay-blur>
            <template #header>
                <span>Crear nueva zona</span>
            </template>
            <div class="gap-y-2">
                <vs-input v-model="zone.name" placeholder="Nombre de la zona" block />
                <div class="flex items-center mt-6">
                    <vs-switch v-model="zone.bookable" color="success"/>
                    <span class="ml-3"> La zona que puede ser reservada por los propitarios </span>
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
                    <div class="mt-3 border border-slate-200 rounded-xl  p-3 md:pl-8" v-if="zone.bookable">
                        <span class="text-slate-500">Define la franja de tiempo para el uso de la zona:</span>
                        <div class="mt-2">
                            <vs-radio v-model="zone.limited" value="free" color="success"><span class="text-sm">Libre</span></vs-radio>
                        </div>
                        <div class="mt-2 flex gap-x-2">       
                            <vs-radio v-model="zone.limited" value="bySlot" color="success"><span class="text-sm">Tiempo limitado</span></vs-radio>
                            <template v-if="zone.limited === 'bySlot'">
                                <vs-input v-model="zone.slotUnits" placeholder="Tiempo" type="number" class="max-w-24"/>
                                <vs-select v-model="zone.slotTime" placeholder="Selecciona...">
                                    <vs-option label="Minutos" value="minutes"> Minutos </vs-option>
                                    <vs-option label="Horas " value="hours"> Horas </vs-option>
                                    <vs-option label="Día copleto" value="fullDay"> Día copleto </vs-option>
                                </vs-select>
                            </template>
                        </div>
                    </div>
                </transition>
            </div>
            <template #footer>
                <div class="flex justify-end gap-x-4">
                    <vs-button 
                    color="dark"
                    type="transparent"
                    @click="showCreateZoneModal =! showCreateZoneModal"
                    >
                    Cancelar
                    </vs-button>
                    <vs-button 
                    color="dark"
                    @click="createZone"
                    >
                    Crear
                    </vs-button>
                </div>
            </template>
        </vs-dialog>
        <vs-dialog v-model="showUpdateZone" overlay-blur>
            <template #header>
                <span>Editar zona</span>
            </template>
            <div class="gap-y-2">
                <vs-input v-model="zone.name" placeholder="Nombre de la zona" block />
                <div class="flex items-center mt-6">
                    <vs-switch v-model="zone.bookable" color="success"/>
                    <span class="ml-3"> La zona que puede ser reservada por los propitarios </span>
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
                    <div class="mt-3 border border-slate-200 rounded-xl  p-3 md:pl-8" v-if="zone.bookable">
                        <span class="text-slate-500">Define la franja de tiempo para el uso de la zona:</span>
                        <div class="mt-2">
                            <vs-radio v-model="zone.limited" value="free" color="success"><span class="text-sm">Libre</span></vs-radio>
                        </div>
                        <div class="mt-2 flex gap-x-2">       
                            <vs-radio v-model="zone.limited" value="bySlot" color="success"><span class="text-sm">Tiempo limitado</span></vs-radio>
                            <template v-if="zone.limited === 'bySlot'">
                                <vs-input v-model="zone.slotUnits" placeholder="Tiempo" type="number" class="max-w-24"/>
                                <vs-select v-model="zone.slotTime" placeholder="Selecciona...">
                                    <vs-option label="Minutos" value="minutes"> Minutos </vs-option>
                                    <vs-option label="Horas " value="hours"> Horas </vs-option>
                                    <vs-option label="Día copleto" value="fullDay"> Día copleto </vs-option>
                                </vs-select>
                            </template>
                        </div>
                    </div>
                </transition>
            </div>
            <template #footer>
                <div class="flex justify-end gap-x-4">
                    <vs-button 
                    color="dark"
                    type="transparent"
                    @click="!showUpdateZone"
                    >
                    Cancelar
                    </vs-button>
                    <vs-button 
                    color="dark"
                    @click="updateZone"
                    >
                    Actualizar
                    </vs-button>
                </div>
            </template>
        </vs-dialog>
    </div>
</template>
<script setup>
    import { ref, shallowRef, watch } from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import EmptyTask from "/src/components/emptys/EmptyTask.vue";
    import IconPlus from "/src/components/icons/IconPlus.vue";
    import IconDotsHorizontal from "/src/components/icons/IconDotsHorizontal.vue";
    import Dropdown from "/src/components/Dropdown.vue"
    import Loading from '/src/components/Loading.vue';
    import { VsNotification } from 'vuesax-alpha'
    
    defineOptions({
        name: 'CommonZones'
    })

    //variables
    const showCreateZoneModal = ref(false)
    const zone = ref({
        name: '',
        bookable: null,
        slotTime: '',
        slotUnits: '',
        limited:null,
    })
    const zones = ref([]);
    const zonesLoading = ref(true);

    //instancia API
    const http = useHttp();
    //user store
    const { user } = useUserStore();

    const showUpdateZone = ref(false);

    //getZones
    async function getZones() { 
    
        try {

            const response = await http.get(`common_areas/${user?.communities[0]?.community_id}/`);
            zones.value = response.data

            zonesLoading.value = false;

        } catch (error) {
        VsNotification({
            position: 'top-right',
            color: 'danger',
            title: 'Upps!! algo ha fallado',
            content: error,
        });
        }
    }
    getZones();

    //createZone
    const createZone = () => {
        
        try {
            const response = http.post(`common_areas/${user?.communities[0]?.community_id}/create/`, { ...zone.value });
            getZones();
            VsNotification({
                position: 'top-right',
                color: 'success',
                title: 'OK',
                content: 'La nueva zona se ha creado con exito',
            });
            zone.value = {
                name: '',
                bookable: null,
                slotTime: '',
                slotUnits: '',
                limited:null,
            }

        } catch (error) {

            VsNotification({
                position: 'top-right',
                color: 'danger',
                title: 'Upps!! algo ha fallado',
                content: error,
            });
        }
    showCreateZoneModal.value = false;
  
    } 
    //editZone
const openUpdateZone = (item) => {
    showUpdateZone.value = true;
    console.log ('item', item)
    zone.value = item 
    
} 
const UpdateZone = () => {
    try {
            
    } catch (error) {
            
        }
} 
        //deleteZone

const deleteZone = (zone) => {
    try {
        const response = http.delete(`common_areas/${user?.communities[0]?.community_id}/${zone.id}/`);
        
            VsNotification({
                position: 'top-right',
                color: 'success',
                title: 'OK',
                content: 'La zona se ha eliminado con exito',
            });
    } catch (error) {
            VsNotification({
                position: 'top-right',
                color: 'danger',
                title: 'Upps!! algo ha fallado',
                content: error,
            });
    }
        getZones();
    } 
</script>
