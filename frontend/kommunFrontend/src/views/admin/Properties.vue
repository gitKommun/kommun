<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
      </div>
      <div class=" p-4 flex justify-end">
        <Button severity="contrast" raised  class="inline flex-none">
          <IconPlus/>
          Añadir propiedad
        </Button>
      </div>
    </div>
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
import IconPlus from "/src/components/icons/IconPlus.vue";
defineOptions({
  name: 'properties',
  layout: Main
})
const title =ref('Propiedades')
</script>

