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
                    @click.capture="open"
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
        <Dialog v-model:visible="showUpdateFolder" modal header="Actualizar carpeta" class="w-96">

            <div class="">
              <InputText v-model="folderName" placeholder="Folder name" :invalid="folderUpdateValidated" variant="filled"/>
            </div>
            <template #footer>
              <div class="flex justify-end gap-x-4">
                <Button 
                  text
                  severity="secondary"
                  label="Cancelar"
                  @click="showUpdateFolder =!showUpdateFolder"
                  />
                <Button 
                  severity="contrast"
                  label="Actualizar"
                  @click="updateFolder()"
                  :loading="folderUpdateLoading"
                  />
              </div>
            </template>
          </Dialog> 
                
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
    import { useToast } from 'primevue/usetoast';

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

 //use toast
    const toast = useToast();

    const emit = defineEmits(['update:items']);
    
    // Delete Item
    function deleteFolder() {
        try {
            const response =  http.delete(`documents/${user?.available_communities[0]?.community_id}/folders/${props.folder.folder_id}/delete`);
            toast.add({ severity: 'success', summary: 'Ok', detail: 'La carpeta se ha eliminado con exito', life: 3000 });
             
        } catch (error) {
            toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
        }
        emit('update:items', true);
    }


    // Update Item
    function updateFolder() {
        folderUpdateLoading.value = true;
        if (folderName.value != '') {
            try {
                const response = http.put(`documents/${user?.available_communities[0]?.community_id}/folders/${props.folder.folder_id}/update/`,
                    {
                        name:folderName.value
                    }
                );
                folderUpdateLoading.value = false;
                showUpdateFolder.value = false;
                toast.add({ severity: 'success', summary: 'Ok', detail: 'La carpeta se ha actualizado con exito', life: 3000 });
               
            } catch (error) {
                toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
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