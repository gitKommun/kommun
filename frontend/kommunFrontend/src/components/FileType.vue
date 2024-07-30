<template>
    <div class="h-8 w-8 flex justify-center items-center rounded-lg"
            :class="setItemClass()">
        <component :is="setIcon()" class="scale-75"/>
    </div>
</template>
<script setup>
import { ref, shallowRef,computed, watch} from 'vue'

import IconFileCSV from '/src/components/icons/IconFileCSV.vue'
import IconFileDOC from '/src/components/icons/IconFileDOC.vue'
import IconFileDOCX from '/src/components/icons/IconFileDOCX.vue'
import IconFileJPG from '/src/components/icons/IconFileJPG.vue'
import IconFilePDF from '/src/components/icons/IconFilePDF.vue'
import IconFilePNG from '/src/components/icons/IconFilePNG.vue'
import IconFileTXT from '/src/components/icons/IconFileTXT.vue'
import IconFileXLS from '/src/components/icons/IconFileXLS.vue';


defineOptions({
    name: 'FileType',
})

const props = defineProps({
        type: {
            type: String
        },
});

const setIcon = () => {
    switch (props.type) {
        case 'PNG':
            return IconFilePNG
            break;
        case 'JPG':
            return IconFileJPG
            break;
        case 'PDF':
            return IconFilePDF
            break;
        case 'DOC':
            return IconFileDOC
            break;
        case 'DOCX':
            return IconFileDOCX
            break;
        case 'TXT':
            return IconFileTXT
            break;
        case 'CSV':
            return IconFileCSV
            break;
        case 'XLS':
            return IconFileXLS
            break;
    
        default:
            break;
    }
    
};

const setItemClass = () => {
    switch (props.type) {
        case 'PNG':
            return 'bg-purple-100 text-purple-500'
            break;
        case 'JPG':
            return 'bg-indigo-100 text-indigo-500'
            break;
        case 'PDF':
            return 'bg-red-100 text-red-500'
            break;
        case 'DOC':
            return 'bg-blue-100 text-blue-500'
            break;
        case 'DOCX':
            return 'bg-sky-100 text-sky-500'
            break;
        case 'TXT':
            return 'bg-cyan-100 text-cyan-500'
            break;
        case 'CSV':
            return 'bg-lime-100 text-lime-500'
            break;
        case 'XLS':
            return 'bg-green-100 text-green-500'
            break;
    
        default:
            break;
    }

}

</script>