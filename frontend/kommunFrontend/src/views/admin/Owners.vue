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
        <vs-table>
            <template #thead>
              <vs-tr>
                <vs-th>  </vs-th>
                <vs-th> Name </vs-th>
                <vs-th> apellidos </vs-th>
                <vs-th> Email </vs-th>
                <vs-th> Rol </vs-th>
                <vs-th class="max-w-12 pr-2">  </vs-th>
              </vs-tr>
            </template>
            <template #tbody>
            <vs-tr v-for="(owner, i) in owners" :key="i" :data="user">
              <vs-td>
                <vs-avatar color="rgb(59,222,200)">
                  <!-- <img :src="'public/'+tr.avatar" alt="" /> -->
                   <template #text> {{user.name}} </template>
                </vs-avatar>
              </vs-td>
              <vs-td>
                {{ owner.name }}
              </vs-td>
              <vs-td>
                {{ owner.surname }}
              </vs-td>
              <vs-td>
                {{ owner.email }}
              </vs-td>
              <vs-td>
                <Tag :color="rolTag(owner.role)">
                  {{ owner.role }}
                </Tag>
              </vs-td>
              <vs-td class="max-w-12 pr-2">
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
                                @click="openUpdateOwner(owner)"
                            >
                                <IconPencil class="scale-75"/>
                                <span>Editar</span>
                            </div>
                            <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                                @click="deleteOwner(owner)"
                                >
                                <IconTrash class="scale-75"/>
                                <span>Eliminar</span>
                            </div>
                        </div>
                    </template>
                </Dropdown>
              </vs-td>

              
            </vs-tr>
      </template>
        </vs-table>
    </div>
    
  </div>  
</template>
<script setup>
  import { ref , shallowRef, reactive, onMounted} from 'vue'
  import Main from '/src/layouts/Main.vue';
  import AddNewOwner from '/src/components/owners/AddNewOwner.vue';
  import { useHttp } from '/src/composables/useHttp.js'; 
  import { useUserStore } from '/src/stores/useUserStore.js';
  import { VsNotification } from 'vuesax-alpha'
  import Tag from "/src/components/Tag.vue"
  import IconDotsHorizontal from "/src/components/icons/IconDotsHorizontal.vue";
  import Dropdown from "/src/components/Dropdown.vue"

  defineOptions({
    name: 'members',
    layout: Main
  })

  //variables
  const title = ref('Propietarios')
  const owners = ref([]);
  const owner = ref({});
  const showCreateOwner = ref(false)
  //Instancia API
  const http = useHttp();
  //user store
  const { user } = useUserStore();
  
  const tagColor = {
    "admin": 'purple',
    "owner": 'blue',
    "tenant": 'emerald',
    "temp":'amber'
  }
  //get owners

  const getOwners = async () => {
    try {

      const response = await http.get(`communities/${user?.communities[0]?.community_id}/users/`);
      owners.value = response.data
      
    } catch (error) {
      VsNotification({
          position: 'top-right',
          color: 'danger',
          title: 'Upps!! algo ha fallado',
          content: error,
      });
    }
  }

  getOwners();

  //delete owner  
  const deleteOwner = async () => {
    try {

      const response = await http.get(`communities/${user?.communities[0]?.community_id}/users/`);
      
    } catch (error) {
      VsNotification({
          position: 'top-right',
          color: 'danger',
          title: 'Upps!! algo ha fallado',
          content: error,
      });
    }
  }

  //update owner  

  const openUpdateOwner = (item) => {
    showUpdateOwner.value = true;
    owner.value = item 
    
  } 
  const updateOwner = async () => {
    try {

      //const response = await http.put(`communities/${user?.communities[0]?.community_id}/users/`);
      
      
    } catch (error) {
      VsNotification({
          position: 'top-right',
          color: 'danger',
          title: 'Upps!! algo ha fallado',
          content: error,
      });
    }
  }

function updateOwners() {
  setTimeout(() => {
    getOwners();
  }, 300);
}

const rolTag = (rol) => {
  return tagColor[rol];
}

</script>

