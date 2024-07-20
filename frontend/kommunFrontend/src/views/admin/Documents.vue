<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.communities[0]?.community_name }}</span>
      </div>
      <div class="w-full p-4 flex justify-end">
        <AddContent 
          @update:items="updateItems" 
          class="h-auto"
          :selected="selectedFolder"
          />  
      </div>
    </div>
    <!-- breadcrum -->
    <div class="flex overflow-x-scroll px-14 -mt-4">
        <div class="flex items-center px-2 text-xs rounded-lg hover:bg-slate-100 transition-all duration-300">
            <IconFolders class="scale-75 text-slate-500"/>
            <span class="ml-2 text-slate-500">Documentos</span>
        </div>
        <template v-for="(e,index) in demo" :key="e">
          <IconChevronRight class="scale-75 mx-1 text-slate-500"/>
          <div class="flex items-center px-2 text-xs rounded-lg hover:bg-slate-100 transition-all duration-300">
            <IconFolder class="scale-75 " :class="index== demo.length-1?'text-lime-500':'text-slate-500'"/>
            <span class="ml-2"  :class="index== demo.length-1?'text-lime-500':'text-slate-500'">{{e}}</span>
          </div>
        </template>
    </div>
    <!-- breadcrum -->

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
                  @click="selectFolder(folder)"
                  
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
import Main from '/src/layouts/Main.vue';
import IconChevronRight from '@/components/icons/IconChevronRight.vue'
import IconFolder from '@/components/icons/IconFolder.vue'
import IconFolders from '@/components/icons/IconFolders.vue'

import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';


// options
defineOptions({
  name: 'documents',
  layout: Main
})

const demo =ref(['demo', 'demo1','demo2'])

//variables
const title = ref('Documentos')
const folders = ref([]);
const foldersLoading = ref(true);
const selectedFolder = ref(null)


//instancia API
const http = useHttp();
//user store
const { user } = useUserStore();
//use toast
const toast = useToast();

// folders
async function getFolders() { 
  if (selectedFolder?.value) {
    try {
    const response = await http.get(`documents/${user?.communities[0]?.community_id}/folders/${selectedFolder?.value.folder_id}`);
    
    folders.value = response.data

    foldersLoading.value = false;
    
  } catch (error) {
    toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
  }
  } else {
    try {
      const response = await http.get(`documents/${user?.communities[0]?.community_id}/folders/`);
      
      folders.value = response.data

      foldersLoading.value = false;
      
    } catch (error) {
      toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
  }
}
getFolders();

function updateItems() {
  setTimeout(() => {
    getFolders();
  }, 300);
}

const selectFolder = (folder) => {
  selectedFolder.value = folder;
  updateItems()
}







</script>

