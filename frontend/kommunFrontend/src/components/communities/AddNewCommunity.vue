<template>
    <div class="">
        <Button severity="contrast" @click="showCreateCommunity =!showCreateCommunity" raised>
            <IconPlus/>
            <span class="hidden md:flex">Nueva Comunidad</span> 
        </Button>
        <Dialog v-model:visible="showCreateCommunity" modal header="Crear nueva comunidad" class="w-96">
            <div class="mb-4">
              <InputText 
                v-model="communityName" 
                placeholder="Name" 
                class="w-full"
                variant="filled"/>
            </div>
              <div class="flex justify-end gap-x-4">
                <Button 
                  text
                  severity="secondary"
                  @click="showCreateCommunity =!showCreateCommunity"
                  label="Cancelar"
                  />
                <Button 
                  severity="contrast"
                  @click="createCommunity"
                  :loading="communityCreateLoading"
                  label="Crear"
                  />
              </div>
          </Dialog> 
    </div>
</template>
<script setup>
import { ref, watch, computed} from 'vue'
import IconPlus from "/src/components/icons/IconPlus.vue";
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';

defineOptions({
    name: 'AddNewCommunity',
})

//variables
const showCreateCommunity = ref(false);
const communityCreateLoading = ref(false);
const communityName= ref('')

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
//emits
const emit = defineEmits(['update:communities']);

const createCommunity = async () => {
    communityCreateLoading.value =true 
    if (communityName.value !== '') {
        try {
            const respone = await http.post(`communities/${user?.current_community?.community_id}/add-user/`, form.value);
            toast.add({ severity: 'success', summary: 'Ok', detail: 'Has creado una nueva comunidad', life: 3000 });
            
        } catch (error) {
            toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
        }
        showCreateCommunity.value = false;
        communityCreateLoading.value = false 
        communityName.value = ''
    }
}

</script>