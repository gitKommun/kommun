<template>
  <div class="h-full w-full">
    <div class="text-slate-950 text-3xl font-bold truncate pl-4 md:pl-16 py-6 flex flex-col">
      {{title}}
      <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
    </div>
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
defineOptions({
  name: 'incidences',
  layout: Main
})
const title =ref('Incidencias')
</script>

