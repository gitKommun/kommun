<template>
    <div class="flex items-center border border-slate-200 p-2 rounded-2xl gap-x-3 mb-3 w-full max-w-72 bg-slate-100  hover:shadow-lg hover:bg-slate-50 relative group cursor-pointer transition-all duration-300">
        <div class="h-12 w-12 flex flex- items-start  justify-center rounded-xl">
            <IconFolder class="text-lime-500"></IconFolder>
        </div>
        <div class="flex flex-col w-full truncate">
            <span class="mb-1 truncate font-semibold text-sm">{{folder.name}}</span>
            <span v-if="folder.document_count === 0" class="text-xs text-slate-500">Carpeta vacia</span>
            <span v-else class="text-xs text-slate-500">{{ folder.document_count }} Elementos</span>
        </div>

        <Dropdown strategy="fixed">
            <template #reference="{ open }">
                <div 
                    class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer "
                    @click="open"
                >
                    <IconDots class="text-slate-500"/>
                </div>
            </template>

            <template #content="{ close }">
                <div class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm">
                    <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                        @click="showUpdateFolder =!showUpdateFolder"
                    >
                        <IconPencil class="scale-75"/>
                        <span>Editar</span>
                    </div>
                    <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                        @click="deleteFolder()"
                        >
                        <IconTrash class="scale-75"/>
                        <span>Eliminar</span>
                    </div>
                </div>
            </template>
        </Dropdown>
        <vs-dialog v-model="showUpdateFolder" overlay-blur>
            <template #header>
              <span>Actualizar carpeta</span>
            </template>
            <div class="">
              <vs-input v-model="folderName" placeholder="Folder name" block>
                <template v-if="folderUpdateValidated" #message-danger> No puedes crear una carpeta sin nombre</template>
              </vs-input>
            </div>
            <template #footer>
              <div class="flex justify-end gap-x-4">
                <vs-button 
                  color="dark"
                  type="transparent"
                  @click="showUpdateFolder =!showUpdateFolder"
                  >
                  Cancelar
                </vs-button>
                <vs-button 
                  color="dark"
                  @click="updateFolder()"
                  :loading="folderUpdateLoading"
                  >
                  Actualizar
                </vs-button>
              </div>
            </template>
          </vs-dialog> 
                
    </div>
</template>
<script setup>
    import { ref, shallowRef, watch } from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import EventBus from '/src/utils/event-bus.js'

    import IconFolder from "/src/components/icons/IconFolder.vue";
    import IconDots from "/src/components/icons/IconDots.vue"
    import IconPencil from "/src/components/icons/IconPencil.vue"
    import IconTrash from "/src/components/icons/IconTrash.vue"
    import Dropdown from "/src/components/Dropdown.vue"
    import { VsNotification } from 'vuesax-alpha'

    // options
    defineOptions({
        name: 'FolderItem',
    })

    const props = defineProps({
        folder: {
            type: Object,
            
        },
    });
//variables
    const showUpdateFolder = ref(false);
    const folderUpdateLoading = ref(false);
    const folderUpdateValidated = ref(false);
    const folderName = ref(props.folder.name);

    //instancia API
    const http = useHttp();
    //user store
    const { user } = useUserStore();

    const emit = defineEmits(['update:items']);
    
    // Delete Item
    function deleteFolder() {
        try {
            const response =  http.delete(`documents/${user?.communities[0]?.community_id}/folders/${props.folder.id}/delete`);
            VsNotification({
                position: 'top-right',
                color: 'success',
                title: 'OK',
                content: 'La carpeta se ha eliminado con exito',
                
            });
             
        } catch (error) {
            VsNotification({
                position: 'top-right',
                color: 'danger',
                title: 'Upps!! algo ha fallado',
                content: error,
            });
        }
        emit('update:items', true);
    }


    // Update Item
    function updateFolder() {
        folderUpdateLoading.value = true;
        if (folderName.value != '') {
            try {
                const response = http.put(`documents/${user?.communities[0]?.community_id}/folders/${props.folder.id}/update/`,
                    {
                        name:folderName.value
                    }
                );
                folderUpdateLoading.value = false;
                showUpdateFolder.value = false;
                VsNotification({
                    position: 'top-right',
                    color: 'success',
                    title: 'OK',
                    content: 'La carpeta se ha actualizado con exito',
                });
                 
               
            } catch (error) {
                VsNotification({
                    position: 'top-right',
                    color: 'danger',
                    title: 'Upps!! algo ha fallado',
                    content: error,
                });
                folderUpdateLoading.value = false;
            }
            emit('update:items', true);
        } else {
            folderUpdateValidated.value = true;
            folderUpdateLoading.value = false;
        }       
    }
    watch(showUpdateFolder, (n, o) => {
        if (!n) {
            folderUpdateValidated.value = false
        }
    })



</script>