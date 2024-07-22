<template>
  <div class="h-full w-full overflow-y-scroll">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full flex flex-col">
          <span class="text-slate-950 text-3xl font-bold truncate flex items-center">{{title}}</span>
          <span class="text-sm text-slate-500 font-medium">{{ user.available_communities[0]?.community_name }}</span>
      </div>
    </div>
    <div class="flex justify-center px-3 pb-6">
      <div class="w-full max-w-4xl flex flex-col gap-y-3">
        <!-- DATOS PERSONALES -->
          <PersonalData/>
          <!-- DATOS GENERALES -->
          <!-- PROPIEDADES -->
           <MyProperties/>
          <!-- PROPIEDADES -->
      </div>
      
    </div>
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
import { useUserStore } from '/src/stores/useUserStore.js';
import IconHome from "/src/components/icons/IconHome.vue"
import IconGarage from "/src/components/icons/IconGarage.vue"
import IconWarehouse from "/src/components/icons/IconWarehouse.vue"
import { useHttp } from '/src/composables/useHttp.js'; 
import PersonalData from '/src/components/profile/PersonalData.vue'
import MyProperties from '/src/components/profile/MyProperties.vue'

const { user } = useUserStore();

defineOptions({
  name: 'Profile',
  layout: Main
})
const title = ref('Mi perfil')

const form = ref({
    name: user.name,
    surname: user.surnames,
    email: user.email,
    phone: user.phoneNumber,
    identificationNumber: user.documentID ?user.documentID : '',
    identificationType: user.documentType ?user.documentType : '',
    allowSharing:user.contactIsPublic   
})


</script>

