<template>
    <div class="w-full">
        <div class="w-full bg-slate-50 p-3 flex gap-x-3 rounded-xl cursor-pointer text-sm font-normal items-center group hover:bg-lime-50 transition-all duration-150"
            @click="showCreateFolder =!showCreateFolder"
        >
            <IconFolderAdd class="group-hover:text-lime-500 transition-all duration-150"/>
            <span class="group-hover:text-lime-500 transition-all duration-150">Nueva carpeta</span>
        </div>
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
    
    
</template>
<script setup>
    import { ref, watch} from 'vue'
    import IconFolderAdd from "/src/components/icons/IconFolderAdd.vue"
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import { VsNotification } from 'vuesax-alpha'

    // options
    defineOptions({
    name: 'addNewFolder',
    })

    //variables
    const showCreateFolder = ref(false);
    const folderName = ref('');
    const folderCreateValidated = ref(false);
    const folderCreateLoading = ref(false);

    //instancia API
    const http = useHttp();
    //user store
    const { user } = useUserStore();

    const emit = defineEmits(['update:folder']);

    watch(showCreateFolder, (n, o) => {
        if (!n) {
            folderCreateValidated.value = false
        }
    })

    // createFolders
    const crateFolder = async () => {
    folderCreateLoading.value = true;
    
    if (folderName.value != '') {
        try {
            const response = await http.post(`documents/${user?.communities[0]?.community_id}/folders/create/`, {
            name: folderName.value
            })
            folderCreateLoading.value = false;
            showCreateFolder.value = false;
            folderName.value = '';
            emit('update:folder', true);
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
        folderCreateValidated.value = true;
        folderCreateLoading.value = false;
    }

  
  
}
</script>