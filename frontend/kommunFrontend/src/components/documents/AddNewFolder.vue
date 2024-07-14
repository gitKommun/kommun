<template>
    <div class="w-full">
        <div class="w-full bg-slate-50 p-3 flex gap-x-3 rounded-xl cursor-pointer text-sm font-normal items-center group hover:bg-lime-50 transition-all duration-150"
            @click="showCreateFolder =!showCreateFolder"
        >
            <IconFolderAdd class="group-hover:text-lime-500 transition-all duration-150"/>
            <span class="group-hover:text-lime-500 transition-all duration-150">Nueva carpeta</span>
        </div>
        <Dialog v-model:visible="showCreateFolder" modal header="Crear nueva carpeta" class="w-96">
            <div class="">
              <InputText v-model="folderName" placeholder="Folder name" :invalid="folderCreateValidated" class="w-full" />
            </div>
              <div class="flex justify-end gap-x-4 pt-4">
                <Button 
                  @click="showCreateFolder =!showCreateFolder"
                  text
                  severity="secondary"
                  >
                  Cancelar
                </Button>
                <Button 
                  @click="crateFolder"
                  :loading="folderCreateLoading"
                  severity="contrast"
                  >
                  Crear
                </Button>
              </div>
          </Dialog>
          <Toast /> 
    </div>
    
    
</template>
<script setup>
    import { ref, watch} from 'vue'
    import IconFolderAdd from "/src/components/icons/IconFolderAdd.vue"
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import { useToast } from 'primevue/usetoast';

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
    //use toast
    const toast = useToast();
    //emit
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
            toast.add({ severity: 'success', summary: 'Ok', detail: 'Carpeta creada con exito', life: 3000 });
        }
        catch (error) {
            toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
        }
    } else {
        folderCreateValidated.value = true;
        folderCreateLoading.value = false;
    }

  
  
}
</script>