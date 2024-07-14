<template>
  <div class="h-full w-full overflow-y-scroll">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full flex flex-col">
          <span class="text-slate-950 text-3xl font-bold truncate flex items-center">{{title}}</span>
          <span class="text-sm text-slate-500 font-medium">{{ user.communities[0]?.community_name }}</span>
      </div>
      <div class=" p-4 flex justify-end">
        <Button 
          severity="danger"
          class="inline flex-none"
          @click="logout"
          raised>
            Cerrar sesión
          </Button>
      </div>
    </div>
    <div class="flex justify-center px-3 pb-6">
      <div class="w-full max-w-4xl ">
        <!-- DATOS PERSONALES -->
          <PersonalData/>
          <!-- DATOS GENERALES -->
          <!-- PROPIEDADES -->
          <!-- ZONAS COMUNES -->
          <div class="p-4 border border-slate-200 rounded-2xl mb-3">
            <div class="flex flex-col">
              <h3 class="text-slate-950 text-xl font-bold">Mis propiedades</h3>
              <p class="text-slate-500">Estas son las propiedades que tienes en la comunidad.</p>
            </div>
            <div class="gap-y-2">
                <div  class="w-full flex flex-col items-center justify-center py-16">
                  <EmptyTask class="scale-75"/>
                  <span class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300">
                      Actualmente no hay propiedades
                  </span>
                  <span class="text-sm text-slate-500 max-w-80 text-center mb-3">
                      Actualmente aun no tienes propiedades vinculadas en está comunidad
                  </span>
                </div>
                <!-- <div class="flex justify-center space-x-4 ">
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
                </div> -->
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
import PersonalData from '/src/components/profile/PersonalData.vue'

const { user } = useUserStore();

defineOptions({
  name: 'Profile',
  layout: Main
})
const title = ref('Mi perfil')
const logoutLoading = ref(false);

const form = ref({
    name: user.name,
    surname: user.surnames,
    email: user.email,
    phone: user.phoneNumber,
    identificationNumber: user.documentID ?user.documentID : '',
    identificationType: user.documentType ?user.documentType : '',
    allowSharing:user.contactIsPublic   
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

