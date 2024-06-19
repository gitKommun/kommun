<template>
  <div class="h-full w-full flex flex-col">
    <div class="text-slate-950 text-3xl font-bold truncate pl-4 md:pl-16 py-6 flex flex-col">
      {{title}}
      <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
    </div>
    <div class=" w-full flex justify-center px-4 flex-1 min-h-0 overflow-y-scroll">
      <div class="w-full max-w-4xl  flex flex-col">
        <div class="flex items-center justify-between py-4">
          <span class="text-slate-950 font-semibold text-lg">Carpetas</span>
          <vs-button
            color="dark"
            size="small"
            type="border"
            @click="showCreateFolder =!showCreateFolder"
            >
            <IconFolderAdd class="scale-75"/>
            <span class="hidden md:flex">Añadir carpeta</span>
          </vs-button>
          <vs-dialog v-model="showCreateFolder" overlay-blur>
            <template #header>
              <span>Crear nueva carpeta</span>
            </template>
            <div class="">
              <vs-input v-model="folderName" placeholder="Folder name" block>
                <template v-if="folderCreateValidated" #message-danger> No puedes crear una carpeta sin nombre</template>
              </vs-input>
            </div>
            <template #footer>
              <div class="flex justify-end gap-x-4">
                <vs-button 
                  color="dark"
                  type="transparent"
                  @click="showCreateFolder =!showCreateFolder"
                  >
                  Cancelar
                </vs-button>
                <vs-button 
                  color="dark"
                  @click="crateFolder"
                  :loading="folderCreateLoading"
                  >
                  Crear
                </vs-button>
              </div>
            </template>
          </vs-dialog>  
        </div>
        <div v-if="foldersLoading" class="flex items-center justify-center py-24 ">
          <Loading/>
        </div>  
        <div v-else class="flex flex-wrap gap-x-4">
          <template v-if="!folders.length">
            <div  class="flex items-center justify-center py-24">
                <EmptyFolder/>
            </div>
          </template>
          <template v-else>
              <div v-for="folder in folders" 
              :key="folder.id"
                  class="flex border border-slate-200 p-3 rounded-2xl gap-x-3 mb-3 w-full max-w-72  hover:shadow-lg hover:bg-slate-50 relative group cursor pointer transition-all duration-300">
                <div class="h-12 w-12 flex items-center justify-center rounded-xl bg-lime-200">
                  <IconFolder class="text-lime-600"></IconFolder>
                </div>
                <div class="flex flex-col">
                  <span class="mb-1 truncate">{{folder.name}}</span>
                  <span class="text-xs text-slate-500">5 Archivos</span>
                </div>
                <div class="h-8 w-8 rounded-xl hover:bg-slate-100 hidden justify-center items-center absolute top-0 right-0 mr-2 mt-2 group-hover:flex transition-all duration-300 cursor-pointer">
                  <IconDots class="text-slate-500"/>
                </div>
              </div>
          </template>
          
        </div>     
        <div class="flex justify-between py-4">
          <span class="text-slate-950 font-semibold text-lg">Archivos</span>
          <vs-button color="dark" size="small" type="border">
            <IconFileAdd class="scale-75"/>
            <span class="hidden md:flex">Añadir archivo</span>
          </vs-button>
          
        </div>
      </div>
      
    </div>
  </div>  
</template>
<script setup>
import { ref, shallowRef, watch } from 'vue'
import IconFolder from "/src/components/icons/IconFolder.vue"
import IconFolderAdd from "/src/components/icons/IconFolderAdd.vue"
import IconFileAdd from "/src/components/icons/IconFileAdd.vue"
import IconDots from "/src/components/icons/IconDots.vue"
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
const showCreateFolder = ref(false);
const folders = ref([]);
const folderName = ref('');
const folderCreateValidated = ref(false);
const folderCreateLoading = ref(false);
const foldersLoading = ref(true);


//instancia API
const http = useHttp();
//user store
const { user } = useUserStore();

// folders
async function getFolders() { 
  
  try {

    const response = await http.get(`documents/${user?.communities[0]?.community_id}/folders/`);

    console.log('reponse folders: ', response);
    folders.value = response.data

    foldersLoading.value = false;
    
  } catch (error) {
    console.log(error);
  }
}
getFolders();


// createFolders
const crateFolder = async () => {
  console.log('entra a crear',)

  folderCreateLoading.value = true;
  if (folderName.value != '') {
      try {
        const response = await http.post(`documents/${user?.communities[0]?.community_id}/folder_create/`, {
          name: folderName.value
        })
        folderCreateLoading.value = false;
        showCreateFolder.value = false;
        getFolders()
      }
      catch (error) {
        VsNotification({
            position: 'top-right',
            color: 'danger',
            title: 'Upps!! algo ha fallado',
            content: error,
        });
      }
  } else {
    folderCreateValidated.value = true
  }
  
}
watch(showCreateFolder, (n, o) => {
  if (!n) {
    folderCreateValidated.value = false
  }
})


</script>

