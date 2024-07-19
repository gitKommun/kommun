<template>
    <div class="">
        <Button severity="contrast" @click="showCreateOwner =!showCreateOwner" raised>
            <IconPlus/>
              Nuevo propietario
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
                    <Select 
                        v-model="form.role" 
                        :options="userTypes" 
                        optionLabel="label" 
                        optionValue="value" 
                        placeholder="Rol..." 
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
    role:''
})
const userTypes = ref([
{ label: 'Administrador', value: 'admin' },
{ label: 'Propietario', value: 'owner' },
{ label: 'Inquilino', value: 'tenant' },
{label:'Temporal',value:'temp'},
])

    //instancia API
    const http = useHttp();
    //user store
    const { user } = useUserStore();

    const emit = defineEmits(['update:owners']);

const createOwner = async () => {
    ownerCreateLoading.value =true 
    if (validatedForm) {
        try {
            const respone = await http.post(`communities/${user?.communities[0]?.community_id}/add-user/`, form.value);
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
            role:''
        }
    }
}
const validatedForm = computed(() => {
    return form.name.value.trim() !== '' &&
        form.surname.value.trim() !== '' &&
        form.role.value.trim() !== '' &&
        form.email.value.trim() !== '' ;
    })
</script>