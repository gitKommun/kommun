<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.communities[0]?.community_name }}"</span>
      </div>
      <div class="w-full p-4 flex justify-end">
        <AddNewOwner @update:owner="updateOwners"/>
      </div>
    </div>
    
    <div class="px-4">
        <DataTable :value="owners" tableStyle="min-width: 50rem">
            <Column field="name" header="Nombre">
              <template #body="slotProps">
                <Avatar label="J" shape="circle"/>
                <span>{{ slotProps.data.name }}</span>
                
              </template>
            </Column>
            <Column field="surname" header="Apellidos"></Column>
            <Column field="email" header="Email"></Column>
            <Column  header="Rol">
              <template #body="slotProps">
                  <!-- <Tag :severity="tagColor[slotProps.data.role]" :value="tagLabel[slotProps.data.role]"></Tag> -->
                  <CustomTag
                  :color="tagColor[slotProps.data.role]"
                  >
                    {{ tagLabel[slotProps.data.role] }}
                  </CustomTag>
              </template>
            </Column>
            <Column field="properties" header="Propiedades vinculadas"></Column>
            <Column header="..." class="flex justify-end" >
              <template #body="slotProps">
                    <Dropdown strategy="fixed">
                        <template #reference="{ open }">
                            <div 
                                class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer "
                                @click="open"
                            >
                                <IconDotsHorizontal class="text-slate-500"/>
                            </div>
                        </template>
                        <template #content="{ close }">
                            <div class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm">
                                <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                                    @click="openUpdateOwner(slotProps.data)"
                                >
                                    <IconPencil class="scale-75"/>
                                    <span>Editar</span>
                                </div>
                                <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                                    @click="deleteOwner(slotProps.data)"
                                    >
                                    <IconTrash class="scale-75"/>
                                    <span>Eliminar</span>
                                </div>
                            </div>
                        </template>
                    </Dropdown>
                </template> 
            </Column>
        </DataTable>
        <Dialog v-model:visible="showUpdateOwner" modal header="Actualizar propietario" class="w-96">
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
                  @click="showUpdateOwner =!showUpdateOwner"
                  label="Cancelar"
                  />
                <Button 
                  severity="contrast"
                  @click="updateOwner"
                  :loading="ownerUpdateLoading"
                  label="Crear"
                  />
              </div>
          </Dialog> 
    </div>
    
  </div>  
</template>
<script setup>
  import { ref , shallowRef, reactive, onMounted} from 'vue'
  import Main from '/src/layouts/Main.vue';
  import AddNewOwner from '/src/components/owners/AddNewOwner.vue';
  import { useHttp } from '/src/composables/useHttp.js'; 
  import { useUserStore } from '/src/stores/useUserStore.js';
import IconDotsHorizontal from "/src/components/icons/IconDotsHorizontal.vue";
  import IconTrash from "/src/components/icons/IconTrash.vue";
    import IconPencil from "/src/components/icons/IconPencil.vue";
import Dropdown from "/src/components/Dropdown.vue";
import { useToast } from 'primevue/usetoast';
import CustomTag from '/src/components/CustomTag.vue'

  defineOptions({
    name: 'members',
    layout: Main
  })

  //variables
  const title = ref('Propietarios')
  const owners = ref([]);
  const owner = ref({
    name: '',
    surname: '',
    email: '',
    password: '1234',
    role:''
  });
  const ownerUpdateLoading = ref(false);
  //Instancia API
  const http = useHttp();
  //user store
const { user } = useUserStore();
        //use toast
    const toast = useToast();
  
  const tagColor = {
    "admin": 'blue',
    "owner": 'lime',
    "tenant": 'amber',
    "temp":'orange'
  }
   const tagLabel = {
    "admin": 'Admin',
    "owner": 'Propietario',
    "tenant": 'Inquilino',
    "temp":'Temporal'
   }
   const userTypes = ref([
    { label: 'Administrador', value: 'admin' },
    { label: 'Propietario', value: 'owner' },
    { label: 'Inquilino', value: 'tenant' },
    {label:'Temporal',value:'temp'},
  ])
const showUpdateOwner = ref(false);
  //get owners

  const getOwners = async () => {
    try {

      const response = await http.get(`communities/${user?.communities[0]?.community_id}/users/`);
      owners.value = response.data
      
    } catch (error) {
     toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
  }

  getOwners();

  //delete owner  
  const deleteOwner = async () => {
    try {

      const response = await http.get(`communities/${user?.communities[0]?.community_id}/users/`);
      
    } catch (error) {
      toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
  }

  //update owner  

const openUpdateOwner = (item) => {
    console.log(item)
  showUpdateOwner.value = true;
    //falta ajustar campos
   // owner.value = item 
    
  } 
  const updateOwner = async () => {
    try {

      //const response = await http.put(`communities/${user?.communities[0]?.community_id}/users/`);
      
      
    } catch (error) {
      toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
  }

function updateOwners() {
  setTimeout(() => {
    getOwners();
  }, 300);
}

</script>

