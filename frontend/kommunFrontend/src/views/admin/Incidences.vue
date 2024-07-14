<template>
  <div class="h-full w-full relative">
    <div class="pl-4 md:pl-16 py-6 flex ">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.communities[0]?.community_name }}</span>
      </div>
      <div class="w-full p-4 flex justify-end">
        <!-- <AddContent @update:items="updateItems" class="h-auto"/>   -->
      </div>
    </div>
    <div class="w-full flex justify-center px-4 flex-1 min-h-0 overflow-y-scroll">
      <div class="w-full max-w-4xl  flex flex-col">
        <!-- resumen -->
        <div class="flex gap-x-3">
          <div class="flex w-1/3 flex-col rounded-2xl bg-slate-50 justify-center items-center py-4">
            <span class="text-xs text-red-500 uppercase">Pendientes</span>
            <span class="text-2xl font-bold">12</span>
          </div>
          <div class="flex w-1/3 flex-col rounded-2xl bg-slate-50 justify-center items-center py-4">
            <span class="text-xs text-amber-500 uppercase">Tramitando</span>
            <span class="text-2xl font-bold">7</span>
          </div>
          <div class="flex w-1/3 flex-col rounded-2xl bg-slate-50 justify-center items-center py-4">
            <span class="text-xs text-green-500 uppercase">Cerradas</span>
            <span class="text-2xl font-bold">48</span>
          </div>
        </div>
        <!-- resumen -->
         <!-- lista incidencias -->
          <div class="w-full">
            <vs-input 
              v-model="search" 
              placeholder="Buscar" 
              label-float 
              />
              
              
          </div>
          <Button @click="openDetail =! openDetail" rised> <IconClose class="group-hover:rotate-90 transition-all duration-300"/> yrryry</Button>
          <!-- lista incidencias -->
      </div>
    </div>
    <!-- detalle -->
     <div 
        class="absolute top-0 right-0 h-full transition-all duration-150 bounce-transition"
        :class="{'w-full md:w-96':openDetail,'w-0 ':!openDetail}"
        >
        <transition
          enter-active-class="transition-all transition-slow ease-out overflow-hidden"
          leave-active-class="transition-all transition-slow ease-in overflow-hidden"
          enter-class="opacity-0 ml-2"
          enter-to-class="opacity-100 ml-0"
          leave-class="opacity-100 ml-0"
          leave-to-class="opacity-0 ml-2"
        >
        <div v-if="openDetail" class="w-full h-full bg-white rounded-xl shadow-2xl p-3">
            <div class="w-full flex  items-center">
                <span class="w-full text-xs text-slate-500 uppercase truncate">Detalle de Incidencia</span>
                <div class="min-h-10 min-w-10 rounded-xl hover:bg-slate-50 flex items-center justify-center transition-all duration-300 group"
                @click="openDetail = false">
                  <IconClose class="group-hover:rotate-90 transition-all duration-300"/>
                </div>
            </div>
        </div>
      </transition>
     </div>
     <!-- detalle -->
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';

import Main from '/src/layouts/Main.vue';
import IconClose from "/src/components/icons/IconClose.vue";

defineOptions({
  name: 'incidences',
  layout: Main
})
const title = ref('Incidencias')
const search = ref('');
const openDetail = ref(false);
//instancia API
const http = useHttp();
//user store
const { user } = useUserStore();
</script>

