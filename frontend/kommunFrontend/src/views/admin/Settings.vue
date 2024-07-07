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
          <GeneralData/>
          <!-- DATOS GENERALES -->
          <!-- PROPIEDADES -->
          <Properties/>
          <!-- PROPIEDADES -->
          <!-- ZONAS COMUNES -->
          <CommonZones/>
          <!-- ZONAS COMUNES -->
      </div>
      
    </div>
  </div>  
</template>
<script setup>
  import { ref, shallowRef } from 'vue'
  import { useHttp } from '/src/composables/useHttp.js'; 
  import { useUserStore } from '/src/stores/useUserStore.js';
  import Main from '/src/layouts/Main.vue';

  import CommonZones from '/src/components/settings/CommonZones.vue'
  import Properties from '/src/components/settings/Properties.vue'
  import GeneralData from '/src/components/settings/GeneralData.vue'

  defineOptions({
    name: 'Settings',
    layout: Main
  })

  //variables
  const title = ref('Configuración')

</script>

