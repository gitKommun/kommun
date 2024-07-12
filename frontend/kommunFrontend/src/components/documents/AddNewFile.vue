<template>
    <div class="w-full">
        <div class="w-full bg-slate-50 p-3 flex gap-x-3 rounded-xl cursor-pointer text-sm font-normal items-center group hover:bg-lime-50 transition-all duration-150"
            @click="showUploadFile =!showUploadFile"
        >
            <IconFileAdd class="group-hover:text-lime-500 transition-all duration-150"/>
            <span class="group-hover:text-lime-500 transition-all duration-150">Subir archivo</span>
        </div>
        <vs-dialog v-model="showUploadFile" overlay-blur>
            <template #header>
              <span>Cargar archivo</span>
            </template>
            <div class="">
              <inputFileDraggable @update:files="updateFiles"/>
            </div>
              <div v-for="(f,i) in files" :key="'k'+i">
                {{ f }}
              </div>
            <template #footer>
              <div class="flex justify-end gap-x-4">
                <vs-button 
                  color="dark"
                  type="transparent"
                  @click="showUploadFile =!showUploadFile"
                  >
                  Cancelar
                </vs-button>
                <vs-button 
                  color="dark"
                  @click="crateFolder"
                  :loading="folderCreateLoading"
                  >
                  Cargar
                </vs-button>
              </div>
            </template>
          </vs-dialog> 
    </div>
    
    
</template>
<script setup>
    import { ref, shallowRef, watch } from 'vue'
    import IconFileAdd from "/src/components/icons/IconFileAdd.vue"
    import inputFileDraggable from '/src/components/inputFileDraggable.vue';
    import EventBus from '/src/utils/event-bus.js'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import { VsNotification } from 'vuesax-alpha'

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
            VsNotification({
                position: 'top-right',
                color: 'danger',
                title: 'Upps!! algo ha fallado',
                content: error,
            });
        }
    
    uploadLoading.value = false;
    showUploadFile.value = false;

  
  
}
</script>