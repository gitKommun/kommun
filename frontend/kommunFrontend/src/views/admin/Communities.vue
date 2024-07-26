<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex ">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.current_community?.community_name }}</span>
      </div>
      <div class="w-full p-4 flex justify-end">
        <AddNewCommunity @update:communities="updateItems" class="h-auto"/>  
      </div>
    </div>
  </div>  
</template>
<script setup>
import { ref, shallowRef } from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';

import Main from '/src/layouts/Main.vue';
import AddNewCommunity from '/src/components/communities/AddNewCommunity.vue'
defineOptions({
  name: 'Communities',
  layout: Main
})
const title = ref('Comunidades')

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
</script>

