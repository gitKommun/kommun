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
              <InputFileDraggable @update:files="updateFiles"/>
            </div>
              <!-- <div v-for="(f,i) in files" :key="'k'+i">
                {{ f.name }}
              </div> -->
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
                  @click="uploadDocument"
                  :loading="uploadLoading"
                  >
                  Cargar
                </Button>
              </div>
            </template>
          </Dialog> 
    </div>
    
    
</template>
<script setup>
    import { ref, shallowRef, watch, toRaw } from 'vue'
    import IconFileAdd from "/src/components/icons/IconFileAdd.vue"
    import InputFileDraggable from '/src/components/InputFileDraggable.vue';
    import EventBus from '/src/utils/event-bus.js'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import { useToast } from 'primevue/usetoast';

    // options
    defineOptions({
    name: 'addNewFolder',
    })
    const props = defineProps({
        selected: {
            type: Object,
            
        },
    });

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

//emit
    const emit = defineEmits(['update:document']);

   const updateFiles = (newFiles) => {
     files.value = newFiles;
     console.log('file',toRaw(files.value))
    };

    // uploadDocument
    const uploadDocument = async () => {
      uploadLoading.value = true;

      if (files.value.length) {
        if (props.selected?.folder_id) {
                    try {
                    const response = await http.post(`documents/${user?.current_community?.community_id}/f/${props.selected.folder_id}/upload/`, {
                      files: toRaw(files.value),
                        //name:

                    }, {
                      headers: {
                          'Content-Type': 'application/json'  // Asegúrate de que este encabezado esté presente
                      }
                    })
                    uploadLoading.value = false;
                    showUploadFile.value = false;
                    files.value = [];
                emit('update:document', true);
                    toast.add({ severity: 'success', summary: 'Ok', detail: 'Documentos cargados con exito', life: 3000 });
                }
                catch (error) {
                    toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
                }
             } else {
                try {
                    const response = await http.post(`documents/${user?.current_community?.community_id}/f/0/upload/`, {
                    files: toRaw(files.value),
                    }, {
                      headers: {
                          'Content-Type': 'application/json'  // Asegúrate de que este encabezado esté presente
                      }
                    })
                    uploadLoading.value = false;
                    showUploadFile.value = false;
                    files.value = [];
                emit('update:document', true);
                    toast.add({ severity: 'success', summary: 'Ok', detail: 'Documentos cargados con exito', life: 3000 });
                }
                catch (error) {
                    toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
                }
            }
      } else {
        toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: 'No has añadido ningun archivo', life: 3000 });
      }    
      uploadLoading.value = false;
      showUploadFile.value = false;

  
  
}
</script>