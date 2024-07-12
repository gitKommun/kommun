<template>
  <div>
    <div
      class="drop-area bg-slate-50 rounded-2xl border-dashed border-2  cursor-pointer flex flex-col items-center justify-center p-12 transition-all duration-150 group"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
      @click="openFilePicker"
      :class="isDragOver?'border-indigo-400':'border-slate-200'"
    >
        <IconUpload class="text-slate-300"/>
        <span class="text-sm text-slate-500 mt-2">Arrastra tus archivos o haz click</span>
      <input type="file" multiple @change="handleFileChange" ref="fileInput" class="hidden" />
    </div>
    <ul class="mt-2 flex flex-col gap-y-1">
        <li v-for="(file, index) in files" 
            :key="file.name"
            class="w-full bg-slate-50 rounded-xl flex items-center justify-between px-3 group"
            >
            
            <span class="w-full truncate text-xs ">{{ file.name }}</span>
            <span class="w-8 h-8 flex justify-center items-center cursor ponter"
                @click="removeFile(index)"    
            >
                <IconTrash class="text-slate-50 group-hover:text-red-500 scale-75 transition-all duration-150 "/>
            </span>
        </li>
    </ul>
  </div>
</template>

<script setup>
    import { ref, watch } from 'vue'
    import IconUpload from "/src/components/icons/IconUpload.vue";
    import IconTrash from "/src/components/icons/IconTrash.vue";
    // options
        defineOptions({
        name: 'inputFileDraggable',
        })
    // variables

    const files = ref([]);
    const isDragOver = ref(false);
    const fileInput = ref(null);

    const emit = defineEmits(['update:files']);

    const handleFileChange = (event) => { 
        files.value = [...event.target.files];
    }
    const handleDragOver = (event) => {
        isDragOver.value = true;
    }
    const handleDragLeave = (event) => { 
        isDragOver.value = false;
    }
    const handleDrop = (event) => {
        isDragOver.value = false;
        const droppedFiles = [...event.dataTransfer.files];
        files.value = [...files.value, ...droppedFiles];
       // emit('update:files', files.value);

    }
    const openFilePicker = () => {
        fileInput.value.click();
    }
    const removeFile = (index) => {
        files.value.splice(index, 1);
       // emit('update:files', files.value);
    }
    watch(files, (n, o) => {
        emit('update:files', files.value);
    })


</script>


