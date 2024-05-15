<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
      </div>
      <div class=" p-4 flex justify-end">
        <vs-button color="dark" class="inline flex-none">Añadir propiedad</vs-button>
      </div>
    </div>
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
defineOptions({
  name: 'properties',
  layout: Main
})
const title =ref('Propiedades')
</script>

