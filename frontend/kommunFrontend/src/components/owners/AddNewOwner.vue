<template>
    <div class="">
        <vs-button color="dark" @click="showCreateOwner =!showCreateOwner">
                <IconPlus class="mr-2"/>
              Nuevo propietario
        </vs-button>
        <vs-dialog v-model="showCreateOwner" overlay-blur>
            <template #header>
              <span>Crear nuevo propietario</span>
            </template>
            <div class="">
              <div class="flex gap-x-3">
                    <vs-input 
                        v-model="form.name" 
                        placeholder="Name" 
                        label-float 
                        block/>
                    <vs-input 
                        v-model="form.surnames" 
                        placeholder="Surname" 
                        label-float 
                        block/>
                </div>
                <vs-input 
                    v-model="form.email" 
                    placeholder="E-mail"
                    type="email"
                    label-float 
                    block/>
                <div class="mt-6">
                    <vs-select v-model="form.role" placeholder="Rol...">
                        <vs-option label="Administrador" value="admin"> Administrador</vs-option>
                        <vs-option label="Propietario" value="owner"> Propietario </vs-option>
                        <vs-option label="Inquilino" value="tenant"> Inquilino</vs-option>
                        <vs-option label="Temporal" value="temp"> Temporal </vs-option>
                    </vs-select>
                </div>
                    
                   
            </div>
            <template #footer>
              <div class="flex justify-end gap-x-4">
                <vs-button 
                  color="dark"
                  type="transparent"
                  @click="showCreateOwner =!showCreateOwner"
                  >
                  Cancelar
                </vs-button>
                <vs-button 
                  color="dark"
                  @click="createOwner"
                  :loading="ownerCreateLoading"
                  >
                  Crear
                </vs-button>
              </div>
            </template>
          </vs-dialog> 
    </div>
</template>
<script setup>
import { ref, watch, computed} from 'vue'
import IconPlus from "/src/components/icons/IconPlus.vue";
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { VsNotification } from 'vuesax-alpha'
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
            VsNotification({
                position: 'top-right',
                color: 'success',
                title: 'Ok',
                content: 'Has creado un nuevo propietario',
            });
            
        } catch (error) {
            VsNotification({
                position: 'top-right',
                color: 'danger',
                title: 'Upps!! algo ha fallado',
                content: error,
            });
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