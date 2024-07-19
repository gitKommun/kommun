<template>
    <div class="w-full">
        <div class="w-full bg-slate-50 p-3 flex gap-x-3 rounded-xl cursor-pointer text-sm font-normal items-center group hover:bg-lime-50 transition-all duration-150"
            @click="showUploadFile =!showUploadFile"
        >
            <IconFileAdd class="group-hover:text-lime-500 transition-all duration-150"/>
            <span class="group-hover:text-lime-500 transition-all duration-150">Subir archivo</span>
        </div>
        <Dialog v-model:visible="showUploadFile" modal header="Cargar archivo" class="w-96">

            <div class="">
              <inputFileDraggable @update:files="updateFiles"/>
            </div>
              <div v-for="(f,i) in files" :key="'k'+i">
                {{ f }}
              </div>
            <template #footer>
              <div class="flex justify-end gap-x-4">
                <Button 
                  text
                  severity="secondary"
                  @click="showUploadFile =!showUploadFile"
                  >
                  Cancelar
                </Button>
                <Button 
                  severity="contrast"
                  @click="crateFolder"
                  :loading="folderCreateLoading"
                  >
                  Cargar
                </Button>
              </div>
            </template>
          </Dialog> 
    </div>
    
    
</template>
<script setup>
    import { ref, shallowRef, watch } from 'vue'
    import IconFileAdd from "/src/components/icons/IconFileAdd.vue"
    import inputFileDraggable from '/src/components/inputFileDraggable.vue';
    import EventBus from '/src/utils/event-bus.js'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import { useToast } from 'primevue/usetoast';

    // options
    defineOptions({
    name: 'addNewFolder',
    })

    //variables
    const showUploadFile = ref(false);
    const files = ref([]);
    const uploadLoading = ref(false);


    //instancia API
    const http = useHttp();
    //user store
    const { user } = useUserStore();
    //use toast
    const toast = useToast();

   const updateFiles = (newFiles) => {
     files.value = newFiles;
      console.log('file', newFiles)
    };

    // uploadDocument
    const uploadDocument = async () => {
      uploadLoading.value = true;
      try {
            // const response = await http.post(`documents/${user?.communities[0]?.community_id}/folders/create/`, {
            // name: folderName.value
            // })
            
        }
        catch (error) {
            toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
        }
    
    uploadLoading.value = false;
    showUploadFile.value = false;

  
  
}
</script>