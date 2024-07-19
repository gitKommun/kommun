<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
      </div>
    </div>
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
import IconPlus from "/src/components/icons/IconPlus.vue";
defineOptions({
  name: 'Providers',
  layout: Main
})
const title =ref('Proveedores')
</script>

