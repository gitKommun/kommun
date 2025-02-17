<template>
  <div class="w-full">
    <div
      class="w-full bg-slate-50 p-3 flex gap-x-3 rounded-xl cursor-pointer text-sm font-normal items-center group hover:bg-indigo-50 transition-all duration-150"
      @click="showUploadFile = !showUploadFile"
    >
      <IconFileAdd
        class="group-hover:text-indigo-500 transition-all duration-150"
      />
      <span class="group-hover:text-indigo-500 transition-all duration-150"
        >Subir archivo</span
      >
    </div>
    <Dialog
      v-model:visible="showUploadFile"
      modal
      header="Cargar archivo"
      class="w-96"
    >
      <div class="">
        <InputFileDraggable @update:files="updateFiles" />
      </div>
      <!-- <div v-for="(f,i) in files" :key="'k'+i">
                {{ f.name }}
              </div> -->
      <template #footer>
        <div class="flex justify-end gap-x-4">
          <Button
            text
            severity="secondary"
            @click="showUploadFile = !showUploadFile"
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
import { ref, shallowRef, watch, toRaw } from "vue";
import IconFileAdd from "/src/components/icons/IconFileAdd.vue";
import InputFileDraggable from "/src/components/InputFileDraggable.vue";
import EventBus from "/src/utils/event-bus.js";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

// options
defineOptions({
  name: "addNewFolder",
});
const props = defineProps({
  selected: {
    type: Object,
  },
});

//variables
const showUploadFile = ref(false);
const files = ref([]);
const uploadLoading = ref(false);

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const emit = defineEmits(["update:document"]);

const updateFiles = (newFiles) => {
  files.value = newFiles;
  console.log("file", toRaw(files.value));
};

// uploadDocument
// const uploadDocument = async () => {
//   uploadLoading.value = true;

//   if (files.value.length) {
//     // Crear FormData para enviar archivos
//     const formData = new FormData();
//     files.value.forEach((file) => {
//       formData.append('files', file);
//     });

//     try {
//       const url = `documents/${user?.current_community?.community_id}/f/${props.selected?.folder_id || '0'}/upload/`;
//       const response = await http.post(url, formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data', // Header correcto para envío de archivos
//         },
//       });

//       uploadLoading.value = false;
//       showUploadFile.value = false;
//       files.value = [];
//       emit("update:document", true);

//       toast.add({
//         severity: "success",
//         summary: "Ok",
//         detail: "Documentos cargados con éxito",
//         life: 3000,
//       });
//     } catch (error) {
//       console.error('Error al subir:', error);
//       toast.add({
//         severity: "error", // Cambiado de 'danger' a 'error'
//         summary: "¡Ups! Algo ha fallado",
//         detail: error.message || "Error al cargar los archivos",
//         life: 3000,
//       });
//     }
//   } else {
//     toast.add({
//       severity: "warning", // Cambiado de 'danger' a 'warning'
//       summary: "¡Ups! Algo ha fallado",
//       detail: "No has añadido ningún archivo",
//       life: 3000,
//     });
//   }

//   uploadLoading.value = false;
//   showUploadFile.value = false;
// };
const uploadDocument = async () => {
  uploadLoading.value = true;

  if (files.value.length) {
    const formData = new FormData();
    
    // Agrega cada archivo a FormData
    files.value.forEach(file => {
      formData.append("file", file); // "file" debe coincidir con el backend
    });

    try {
      const response = await http.post(
        `documents/${user?.current_community?.community_id}/f/${props.selected?.folder_id || 0}/upload/`,
        formData,  // <-- Aquí enviamos el objeto FormData
        {
          headers: {
            // No agregues 'Content-Type', ya que FormData lo maneja automáticamente
          }
        }
      );
      
      uploadLoading.value = false;
      showUploadFile.value = false;
      files.value = [];
      emit('update:document', true);
      
      toast.add({ severity: 'success', summary: 'Ok', detail: 'Documentos cargados con éxito', life: 3000 });
    } catch (error) {
      toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
  } else {
    toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: 'No has añadido ningún archivo', life: 3000 });
  }

  uploadLoading.value = false;
  showUploadFile.value = false;
};
</script>
