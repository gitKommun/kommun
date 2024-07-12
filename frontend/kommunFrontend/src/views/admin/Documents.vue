<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.communities[0]?.community_name }}</span>
      </div>
      <div class="w-full p-4 flex justify-end">
        <AddContent @update:items="updateItems" class="h-auto"/>  
      </div>
    </div>
    
    <!-- old -->
    <div class=" w-full flex justify-center px-4 flex-1 min-h-0 overflow-y-scroll">
      <div class="w-full max-w-4xl  flex flex-col">
        
        <div v-if="foldersLoading" class="flex items-center justify-center py-24 ">
          <Loading/>
        </div>  
        <div v-else class="flex flex-wrap gap-x-4">
          <template v-if="!folders.length">
            <div  class="w-full flex flex-col items-center justify-center py-24">
              <EmptyFolder class="scale-75"/>
              <span class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300">
                Actualmente no hay documentos
              </span>
              <span class="text-sm text-slate-500 max-w-80 text-center">Comienza ahora creando la estructura de documentacion de tu comunidad</span>
            </div>
          </template>
          <template v-else>
            <div class="w-full flex flex-col">
              <div v-if="folders.length" class="flex items-center justify-between py-4">
                <span class="text-slate-950 font-semibold text-lg">Carpetas</span>
              </div>
              <div class="w-full flex flex-wrap gap-3">
                <FolderItem
                  v-for="folder in folders"
                  :key="folder.id"
                  :folder="folder"
                  @update:items="updateItems"
                />
              </div>
              <div v-if="folders.length" class="flex items-center justify-between py-4">
                  <span class="text-slate-950 font-semibold text-lg">Archivos</span>
              </div>
            </div>    
          </template>
          
        </div>     
      </div>
      
    </div>
  </div>  
</template>
<script setup>
import { ref, watch} from 'vue'

import AddContent from "/src/components/documents/AddContent.vue"
import FolderItem from "/src/components/documents/FolderItem.vue"
import EmptyFolder from "/src/components/emptys/EmptyFolder.vue"
import Loading from '/src/components/Loading.vue'
import { VsNotification } from 'vuesax-alpha'
import Main from '/src/layouts/Main.vue';

import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';


// options
defineOptions({
  name: 'documents',
  layout: Main
})

//variables
const title = ref('Documentos')
const folders = ref([]);
const foldersLoading = ref(true);


//instancia API
const http = useHttp();
//user store
const { user } = useUserStore();

// folders
async function getFolders() { 
  
  try {

    const response = await http.get(`documents/${user?.communities[0]?.community_id}/folders/`);
    folders.value = response.data

    foldersLoading.value = false;
    
  } catch (error) {
    VsNotification({
          position: 'top-right',
          color: 'danger',
          title: 'Upps!! algo ha fallado',
          content: error,
      });
  }
}
getFolders();

function updateItems() {
  setTimeout(() => {
    getFolders();
  }, 300);
}







</script>

