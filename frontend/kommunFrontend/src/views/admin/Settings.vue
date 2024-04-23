<template>
  <div class="h-full w-full overflow-y-scroll">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
      </div>
      <div class=" p-4 flex justify-end">
        <vs-button color="dark" class="inline">Guardar</vs-button>
      </div>
    </div>
    <div class="flex justify-center px-3 pb-6">
      <div class="w-full max-w-4xl ">
        <!-- DATOS GENERALES -->
          <div class="p-4 border border-slate-200 rounded-2xl mb-3">
            <div class="flex items-center justify-between">
              <h3 class="text-slate-950 text-lg font-semibold"> Datos generales</h3>
            </div>
            <div class="gap-y-2">
                <div class="">
                    <vs-input v-model="form.name" placeholder="Nombre de la comunidad" label-float block/>
                </div>
                <div class="">
                    <vs-input v-model="form.address" placeholder="Dirección" label-float  block/>
                </div>
                <div class="flex gap-x-3 ">
                    <vs-input v-model="form.city" placeholder="Ciudad" label-float  block/>
                    <vs-input v-model="form.postalCode" placeholder="Código postal" label-float  block/>
                </div>
                <div class="flex gap-x-3 ">
                    <vs-input v-model="form.cif" placeholder="CIF" label-float />
                </div>
            </div>
          </div>
          <!-- DATOS GENERALES -->
          <!-- PROPIEDADES -->
          <div class="p-4 border border-slate-200 rounded-2xl mb-3">
            <div class="flex items-center justify-between">
              <h3 class="text-slate-950 text-lg font-semibold">Propiedades</h3>
            </div>
            <div class="gap-y-2 pt-3">
              <div class="md:columns-3 text-xs uppercase text-slate-500 mb-2">
                <div>Tipo</div>
                <transition
                enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                enter-class="opacity-0"
                enter-to-class="opacity-100"
                leave-class="opacity-100"
                leave-to-class="opacity-0"
                mode="out-in"
                >
                <div v-if="form.propertyTypes.length">Cantidad</div>
                </transition>
              </div>
                <div class="columns-1 md:columns-3  mb-2">
                  <vs-checkbox v-model="form.propertyTypes" color="success" value="apartment"> Viviendas </vs-checkbox>
                  <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                  >
                  <vs-input 
                    v-if="form.propertyTypes.includes('apartment')"
                    v-model="form.apartmentAccount" 
                    placeholder="Nº de viviendas"  
                    type="number"
                    />
                  </transition>
                </div>
                <div class="columns-1 md:columns-3 mb-2">
                  <vs-checkbox v-model="form.propertyTypes" color="success" value="garage" > Plazas de aparcamiento </vs-checkbox>
                  <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                  >
                  <vs-input 
                    v-if="form.propertyTypes.includes('garage')"
                    v-model="form.garageAccount" 
                    placeholder="Nº de plazas"  
                    type="number"
                    class="w-12"
                  />
                  </transition>
                </div>
                <div class="columns-1 md:columns-3">
                  <vs-checkbox v-model="form.propertyTypes" color="success" value="storageRoom"> Trasteros </vs-checkbox>
                  <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                  >
                  <vs-input 
                    v-if="form.propertyTypes.includes('storageRoom')"
                    v-model="form.storageRoomAccount" 
                    placeholder="Nº de trasteros"  
                    type="number" 
                    />
                    </transition>
                </div>
            </div>
          </div>
          <!-- PROPIEDADES -->
          <!-- ZONAS COMUNES -->
          <div class="p-4 border border-slate-200 rounded-2xl mb-3">
            <div class="flex flex-col">
              <h3 class="text-slate-950 text-xl font-bold">Zonas comunes</h3>
              <p class="text-slate-500">Regitra tus zonas comunes como piscinas, gimnasio, pista de padel ...</p>
            </div>
            <div class="gap-y-2">
                <div class="w-full flex flex-col justify-center items-center">
                  <EmptyTask/>
                  <p class="text-sm text-slate-500 my-3">Aun no hay registrado ningún elemento como zona comun</p>
                  <vs-button 
                    color="dark" 
                    class="inline"
                    type="border"
                    @click="showCreateZoneModal= true"
                    >Crear elemento</vs-button>
                </div>
                <div class="">
                  <vs-table>
                    <template #thead>
                      <vs-tr>
                        <vs-th> Nombre </vs-th>
                        <vs-th> Reseva </vs-th>
                        <vs-th> tiempo </vs-th>

                      </vs-tr>
                    </template>
                    <template #tbody>
                      <vs-tr v-for="(zone, i) in form.commonZones" :key="i" :data="tr">
                        <vs-td>
                          {{ zone.name }}
                        </vs-td>
                        <vs-td>
                          {{ zone.limited }}
                        </vs-td>
                        <vs-td>
                          {{ zone.slotTime }} {{ zone.slotUnits }}
                        </vs-td>
                      </vs-tr>
                    </template>
                  </vs-table>
                </div>

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
                      <span class="text-slate-500">Define el tiempo de uso de la zona:</span>
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
            </div>
          </div>
          <!-- ZONAS COMUNES -->
      </div>
      
    </div>
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
import EmptyTask from "/src/components/emptys/EmptyTask.vue"
defineOptions({
  name: 'Settings',
  layout: Main
})
const title = ref('Configuración')

const form = ref({
    name: '',
    address: '',
    city:'',
    postalCode: '',
    cif: '',
    propertyTypes: [],
    apartmentAccount: null,
    garageAccount: null,
    storageRoomAccount: null,
    commonZones: ref([])
    
})
const ejem = ref({
    title: 'baaaa',

})
const showCreateZoneModal = ref(false)
const zone = ref({
  name: '',
  bookable: null,
  slotTime: '',
  slotUnits: '',
  limited:null,
})

const createZone = () => {
  
  form.value?.commonZones.push(zone.value);
  showCreateZoneModal.value = false;
  zone.value = {
  name: '',
  bookable: null,
  slotTime: '',
  slotUnits: '',
  limited:null,
}

} 
</script>

