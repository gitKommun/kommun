<template>
  <div class="h-full w-full overflow-y-scroll">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full flex flex-col">
          <span class="text-slate-950 text-3xl font-bold truncate flex items-center">{{user.name}}</span>
          <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
      </div>
      <div class=" p-4 flex justify-end">
        <vs-button color="dark" class="inline flex-none">Guardar</vs-button>
        <vs-button 
          color="danger" 
          class="inline flex-none"
          @click="logout">Cerrar sesión</vs-button>
      </div>
    </div>
    <div class="flex justify-center px-3 pb-6">
      <div class="w-full max-w-4xl ">
        <!-- DATOS PERSONALES -->
          <div class="p-4 border border-slate-200 rounded-2xl mb-3">
            <div class="flex items-center justify-between">
              <h3 class="text-slate-950 text-lg font-semibold"> Datos generales </h3>
            </div>
            {{ user }}
            <div class="gap-y-2">
                <div class="">
                    <vs-input v-model="form.name" placeholder="Nombre" label-float block/>
                    <vs-input v-model="form.surname" placeholder="Apellidos" label-float  block/>
                </div>
                <div class="flex gap-x-3 mb-6">
                    <vs-input v-model="form.email" placeholder="E-mail" label-float  block/>
                    <vs-input v-model="form.phone" placeholder="Teléfono" label-float  block/>
                    
                </div>
                <div class="flex items-center gap-x-2">
                  <vs-select v-model="form.identificationType" placeholder="Selecciona...">
                      <vs-option label="DNI" value="DNI"> DNI </vs-option>
                      <vs-option label="NIE " value="NIE"> NIE </vs-option>
                      <vs-option label="Pasaporte" value="passport"> Pasaporte </vs-option>
                  </vs-select>
                  <vs-input v-model="form.identificationNumber" placeholder="Número de identificación" class="max-w-48"/>
                </div>
                <div class="flex items-center mt-6">
                    <vs-switch v-model="form.allowSharing" color="success"/>
                    <span class="ml-3"> Permitir que los otros propietarios tengan acesso a tus datos de contacto </span>
                </div>
            </div>
          </div>
          <!-- DATOS GENERALES -->
          <!-- PROPIEDADES -->
          <!-- ZONAS COMUNES -->
          <div class="p-4 border border-slate-200 rounded-2xl mb-3">
            <div class="flex flex-col">
              <h3 class="text-slate-950 text-xl font-bold">Mis propiedades</h3>
              <p class="text-slate-500">Estas son las propiedades que tienes en la comunidad.</p>
            </div>
            <div class="gap-y-2">
                <div class="w-full flex flex-col justify-center items-center">
                  <EmptyTask/>
                  <p class="text-sm text-slate-500 my-3">Aun no hay ninguna propiedad vinculada</p>
                  <!-- <vs-button 
                    color="dark" 
                    class="inline"
                    type="border"
                    @click="showCreateZoneModal= true"
                    >Crear elemento</vs-button> -->
                </div>
                <div class="flex justify-center space-x-4 ">
                  <div class="rounded-xl p-3 bg-slate-50 w-72">
                    <div class="flex items-center justify-center flex-col">
                        <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                          <IconHome class="text-blue-500"/>
                        </div>
                        <div class="w-full mt-3">
                          <p class="text-slate-500 flex flex-col">
                            <span>Portal: <span class="font-semibold text-slate-950">45</span></span>
                            <span>Piso: <span class="font-semibold text-slate-950">2º</span></span>
                            <span>Puerta: <span class="font-semibold text-slate-950">A</span></span>
                          </p>
                          
                        </div>
                        <div class="w-full border-t border-slate-200 flex justify-center items-center pt-2 text-xs text-slate-500">
                            Coeficiente:  <span class="text-cyan-500 font-bold text-sm ml-2">1,45%</span>
                        </div>
                    </div>
                  </div>
                  <div class="rounded-xl p-3 bg-slate-50 w-72">
                    <div class=" flex items-center justify-center flex-col">
                        <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
                          <IconGarage class="text-purple-500"/>
                        </div>
                        <div class="w-full mt-3">
                          <p class="text-slate-500 flex flex-col">
                            <span>Plaza: <span class="font-semibold text-slate-950">18</span></span>
                          </p>
        
                        </div>
                        <div class="w-full border-t border-slate-200 flex justify-center items-center pt-2 text-xs text-slate-500">
                            Coeficiente:  <span class="text-cyan-500 font-bold text-sm ml-2">3,21%</span>
                        </div>  
                    </div>
                  </div>
                  <div class="rounded-xl p-3 bg-slate-50 w-72">
                    <div class=" flex items-center justify-center flex-col">
                        <div class="w-12 h-12 rounded-full bg-teal-100 flex items-center justify-center">
                          <IconWarehouse class="text-teal-500"/>
                        </div>
                    </div>
                  </div>
                </div>
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
import { useUserStore } from '/src/stores/useUserStore.js';
import IconHome from "/src/components/icons/IconHome.vue"
import IconGarage from "/src/components/icons/IconGarage.vue"
import IconWarehouse from "/src/components/icons/IconWarehouse.vue"
import { useHttp } from '/src/composables/useHttp.js'; 
import { useRouter } from 'vue-router';
import { VsNotification } from 'vuesax-alpha'

const { user } = useUserStore();

defineOptions({
  name: 'Profile',
  layout: Main
})
const title = ref('perfil')
const logoutLoading = ref(false);

const form = ref({
    name: user.name,
    surname: user.surnames,
    email: user.email,
    phone: user.phoneNumber,
    identificationNumber: user.documentID ?user.documentID : '',
    identificationType: '',
    allowSharing:false    
})

//instancia API
const http = useHttp();

// router
const router = useRouter();

const logout = async () => {
  logoutLoading.value = true
  try {
    await http.post(`members/logout/`)
    logoutLoading.value = false;
    window.location.reload();
  } catch (error) {
    VsNotification({
            position: 'top-right',
            color:'danger',
            title: 'Error de autenticación',
            content:error,
    })
    loginLoading.value = false
  }
}

</script>

