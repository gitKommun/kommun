<template>
    <div class="">
        <Button severity="contrast" @click="showCreateIncidence =!showCreateIncidence" raised>
            <IconPlus/>
             <span class="hidden md:flex">Nueva incidencia</span> 
        </Button>
        <Dialog v-model:visible="showCreateIncidence" modal header="Crear nuevo propietario" class="w-120">
            <div class="">
              <div class="flex gap-x-3 mb-4">
                    <InputText 
                        v-model="form.title" 
                        placeholder="Name" 
                        class="w-full"
                        variant="filled"/>
                </div>
                <Textarea
                    v-model="form.description" 
                    placeholder="Descripción"
                    variant="filled"  
                    class="w-full"/>
                <div class="flex gap-x-3 mt-3">
                    <Select 
                        v-model="form.category" 
                        :options="categories" 
                        optionLabel="label" 
                        optionValue="value" 
                        placeholder="Categoría..." 
                        class="w-full mb-4"
                        variant="filled"/>
                        <Select 
                        v-model="form.priority" 
                        :options="priorities" 
                        optionLabel="label" 
                        optionValue="value" 
                        placeholder="Prioridad" 
                        class="w-full mb-4"
                        variant="filled"
                        >
                        <template #value="slotProps">
                            <div v-if="slotProps.value" class="flex items-center">
                                <CustomTag :color="priorityColor[slotProps?.value]"><IconFlag class="scale-75 -ml-1"/>  {{ priorityLabel[slotProps?.value] }}</CustomTag>
                                <!-- <span class="flex gap-x-2 items-center" :class="statusColor(slotProps?.value)">
                                    <IconFlag/> {{ slotProps?.value }}
                                    {{ slotProps }}
                                </span> -->
                            </div>
                            <span v-else>
                                {{ slotProps.placeholder }}
                            </span>
                        </template>
                        <template #option="slotProps">
                            <CustomTag :color="priorityColor[slotProps.option.value]"><IconFlag class="scale-75 -ml-1"/>  {{ slotProps.option.label }}</CustomTag>
                        </template>
                        </Select>
                </div>

                    
                   
            </div>
              <div class="flex justify-end gap-x-4">
                <Button 
                  text
                  severity="secondary"
                  @click="showCreateIncidence =!showCreateIncidence"
                  label="Cancelar"
                  />
                <Button 
                  severity="contrast"
                  @click="createIncidence"
                  :loading="incidenceCreateLoading"
                  label="Crear"
                  />
              </div>
          </Dialog> 
    </div>
</template>
<script setup>
import { ref, watch, computed} from 'vue'
import IconPlus from "/src/components/icons/IconPlus.vue";
import IconFlag from "/src/components/icons/IconFlag.vue";
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';
 import CustomTag from '/src/components/CustomTag.vue'

defineOptions({
    name: 'AddNewOwner',
})
const getFormattedDate = ()=> {
  const today = new Date();
  const day = String(today.getDate()).padStart(2, '0');
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const year = String(today.getFullYear()).slice(-2);

  return `${day}/${month}/${year}`;
}
//variables
const showCreateIncidence = ref(false);
const incidenceCreateLoading = ref(false);
const form = ref({
    title: '',
    description: '',
    //user: '',
    priority: '',
    category: '',
    status:'reported',
    date: getFormattedDate,
    //community_id:
})
const categories = ref([
{ label: 'Mantenimiento', value: 'maintenance' },
{ label: 'Limpieza', value: 'cleaning' },
{ label: 'Seguridad', value: 'security' },
])

const priorities = ref([
{ label: 'Baja', value: 'low' },
{ label: 'Media', value: 'medium' },
{ label: 'Alta', value: 'high' },
{ label: 'Urgente', value: 'urgent' },
])

const priorityColor = {
    low: 'blue',
    medium: 'yellow',
    high: 'orange',
    urgent:'red'
}
const priorityLabel = {
    low: 'Baja',
    medium: 'Media',
    high: 'Alta',
    urgent:'Urgente'
}


const statusColor = (priority) => {
    switch (priority) {
        case 'low':
            return 'text-blue-500'
            break;
        case 'medium':
            return 'text-amber-500'
            break;
        case 'high':
            return 'text-orange-500'
            break;
        case 'urgent':
            return 'text-red-500'
            break;
    
        default:
            break;
    }
}

    //instancia API
    const http = useHttp();
    //user store
const { user } = useUserStore();
    
  //use toast
    const toast = useToast();

    const emit = defineEmits(['update:owners']);

const createIncidence = async () => {
    incidenceCreateLoading.value =true 
    if (validatedForm) {
        try {
            const respone = await http.post(`claims/${user?.available_communities[0]?.community_id}/create/`, form.value);
            toast.add({ severity: 'success', summary: 'Ok', detail: 'Has creado un nuevo propietario', life: 3000 });
            
        } catch (error) {
            toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
        }
        showCreateIncidence.value = false;
        incidenceCreateLoading.value = false 
        form.value = {
            title: '',
            description: '',
            //user: '',
            priority: '',
            category: '',
            status:'reported',
            date: null,
        }
    }
}

//utilities
const validatedForm = computed(() => {
    return form.title.value.trim() !== '' &&
        form.description.value.trim() !== '' &&
        form.category.value.trim() !== '' &&
        form.priority.value.trim() !== '' ;
})


</script>