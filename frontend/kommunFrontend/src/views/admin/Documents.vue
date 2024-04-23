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
              <vs-input v-model="folderName" placeholder="Folder name" block />
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
                  >
                  Crear
                </vs-button>
              </div>
            </template>
          </vs-dialog>
          
        </div>
        <div class="flex flex-wrap gap-x-4">
          <div v-for="e in 10" class="flex border border-slate-200 p-3 rounded-2xl gap-x-3 mb-3 w-full max-w-72 hover:bg-slate-50">
            <div class="h-12 w-12 flex items-center justify-center rounded-xl bg-lime-200">
              <IconFolder class="text-lime-600"></IconFolder>
            </div>
            <div class="flex flex-col">
              <span class="mb-1 truncate">Estatutos</span>
              <span class="text-xs text-slate-500">5 Archivos</span>
            </div>
        </div>
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
import { ref, shallowRef } from 'vue'
import IconFolder from "/src/components/icons/IconFolder.vue"
import IconFolderAdd from "/src/components/icons/IconFolderAdd.vue"
import IconFileAdd from "/src/components/icons/IconFileAdd.vue"
import Main from '/src/layouts/Main.vue';
defineOptions({
  name: 'documents',
  layout: Main
})
const title = ref('Documentos')
const showCreateFolder = ref(false)
const folderName = ref('')
</script>

