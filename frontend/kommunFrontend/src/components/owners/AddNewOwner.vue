<template>
    <div class="">
        <Button severity="contrast" @click="showCreateOwner =!showCreateOwner" raised>
            <IconPlus/>
            <span class="hidden md:flex">Nuevo usuario</span> 
        </Button>
        <Dialog v-model:visible="showCreateOwner" modal header="Crear nuevo propietario" class="w-96">
            <div class="">
              <div class="flex gap-x-3 mb-4">
                    <InputText 
                        v-model="form.name" 
                        placeholder="Name" 
                        class="w-full"
                        variant="filled"/>
                    <InputText  
                        v-model="form.surnames" 
                        placeholder="Surname" 
                        class="w-full"
                        variant="filled"/>
                </div>
                <InputText  
                    v-model="form.email" 
                    placeholder="E-mail"
                    class="w-full"
                    variant="filled"/>
                <div class="mt-4">
                    <MultiSelect 
                        v-model="form.roles" 
                        :options="userTypes"
                        filter
                        optionLabel="label" 
                        optionValue="value" 
                        placeholder="Select role" 
                        class="w-full mb-4"
                        variant="filled"/>
                </div>
                    
                   
            </div>
              <div class="flex justify-end gap-x-4">
                <Button 
                  text
                  severity="secondary"
                  @click="showCreateOwner =!showCreateOwner"
                  label="Cancelar"
                  />
                <Button 
                  severity="contrast"
                  @click="createOwner"
                  :loading="ownerCreateLoading"
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
    name: 'AddNewOwner',
})

//variables
const showCreateOwner = ref(false);
const ownerCreateLoading = ref(false);
const form = ref({
    name: '',
    surname: '',
    email: '',
    password: '1234',
    roles:[]
})
const userTypes = ref([
{ label: 'Administrador', value: 'admin' },
{ label: 'Propietario', value: 'owner' },
// { label: 'Inquilino', value: 'tenant' },
// {label:'Temporal',value:'temp'},
])

    //utils
    const http = useHttp();
    const { user } = useUserStore();
    const toast = useToast();

    const emit = defineEmits(['update:owners']);

const createOwner = async () => {
    const member = {
        profiles: [
            form.value
        ]
    }
    ownerCreateLoading.value =true 
    if (validatedForm) {
        try {
            const respone = await http.post(`communities/${user?.current_community?.community_id}/neighbors/add/`,member);
            toast.add({ severity: 'success', summary: 'Ok', detail: 'Has creado un nuevo propietario', life: 3000 });
            
        } catch (error) {
            toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
        }
        showCreateOwner.value = false;
        ownerCreateLoading.value = false 
        form.value = {
            name: '',
            surname: '',
            email: '',
            password: '1234',
            roles:[]
        }
         emit('update:owners', true);
    }
}
const validatedForm = computed(() => {
    return form.name.value.trim() !== '' &&
        form.surname.value.trim() !== '' &&
        form.role.value.trim() !== '' &&
        form.email.value.trim() !== '' ;
    })
</script>