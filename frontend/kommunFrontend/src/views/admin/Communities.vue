<template>
  <div class="h-full w-full overflow-y-scroll">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.current_community?.community_name }}</span>
      </div>
      <div class="w-full p-4 flex justify-end">
        <AddNewCommunity @update:communities="updateItems" class="h-auto"/>  
      </div>
    </div>
    <!-- search and view -->
    <div v-if="communities.length" class="flex items-center justify-between pb-4 w-full max-w-4xl mx-auto px-4 ">
      <InputText 
          v-model="search" 
          placeholder="Buscar" 
          variant="filled"/>
      <SelectButton v-model="toggleView" :options="toggleViewOptions" optionLabel="value" >
          <template #option="slotProps">
              <IconGrid v-if="slotProps.option === 'card'"/>
              <IconTable v-else/>
          </template>
      </SelectButton>
    </div>
    <!-- search and view -->
    
     <div class="w-full flex  justify-center px-4 flex-1 min-h-0 ">
       <div class="w-full max-w-4xl  flex flex-col">
          <!-- cards -->
          <div 
           v-if="toggleView === 'card'"
          class=""
          key="cards">
            <transition-group 
              tag="ul"
              class="list-none w-full flex flex-wrap gap-3 pb-4"
              enter-active-class="transition-all transition-slow ease-out overflow-hidden"
              leave-active-class="transition-all transition-slow ease-in overflow-hidden"
              enter-class="opacity-0"
              enter-to-class="opacity-100"
              leave-class="opacity-100"
              leave-to-class="opacity-0"
              mode="out-in">
                <CommunityItem
                v-for ="community in filteredCommunities"
                :key="community.community_id"
                :community="community"
                @update:community="updateItems"
              />

            </transition-group>

            


          </div>
          <!-- cards-->
          <!-- table -->
           <div 
            v-else
            class="w-full"
            key="table">
            <DataTable :value="filteredCommunities" class="text-sm">
              <column header="Comunidad" >
                <template #body="slotProps">
                  <span class="flex flex-col w-full">
                    <span class="flex">
                      <CustomTag
                        v-if="isCurrent(slotProps.data.community_id)"
                        :solid="true"
                        :color="'green'"
                        >
                        Actual
                        </CustomTag>
                      <span class="font-medium" :class="isCurrent(slotProps.data.community_id)?'ml-2':''">{{slotProps.data.name}}</span>
                    </span>
                    <span class="text-xs text-slate-400"> {{slotProps.data.address}}, {{slotProps.data.city}}</span>
                  </span>
                  
                </template>
              </column>
              <column header="otro"></column>
              <column header="Catastro">
                <template #body="slotProps">
                  REF8439393829920202
                </template>
              </column>
              <column header="Propiedades" field="numberProperties">
                <template #body="slotProps">
                  {{ slotProps.data.numberProperties || '0' }}
                </template></column>
              <Column :rowEditor="true" style="width: 10%; min-width: 8rem;" bodyStyle="text-align:right">
                <template #body="slotProps">
                  <Button 
                    v-if="!isCurrent(slotProps.data.community_id)"
                    size="small flex-none"
                    severity="contrast"
                    outlined
                    @click="setCurrent(slotProps.data.community_id)"
                    >
                    Seleccionar
                  </Button>
                </template>
              </column>
              <Column :rowEditor="true" style=" min-width: 4rem; " bodyStyle="text-align:right">
                <template #body="slotProps">
                  <div 
                      class="h-8 w-8 rounded-xl flex items-center justify-center hover:bg-slate-100 transition-all duration-300 group ml-auto"
                      @click="configCommunity(slotProps.data.community_id)"
                      >
                      <IconSettings class="text-slate-400 group-hover:text-slate-950"/>
                  </div>
                </template>
              </column>

            </DataTable>
           </div>
          <!-- table -->
       </div>
     </div>


  </div>  
</template>
<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useUI } from '/src/stores/useUI.js';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';

import Main from '/src/layouts/Main.vue';
import AddNewCommunity from '/src/components/communities/AddNewCommunity.vue'
import CommunityItem from '/src/components/communities/CommunityItem.vue'
import IconTable from '@/components/icons/IconTable.vue'
import IconGrid from '@/components/icons/IconGrid.vue'
import IconSettings from '@/components/icons/IconSettings.vue'
import CustomTag from '/src/components/CustomTag.vue'
defineOptions({
  name: 'Communities',
  layout: Main
})
const title = ref('Comunidades')

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const { communityList, setCommunityList } = useUI();
const route = useRouter();

const communities = ref([]);
const toggleView = ref(communityList);
const toggleViewOptions = ref(['card', 'table'])
const search = ref('')


watch(toggleView, (n) => {
  console.log(setCommunityList);
  //setCommunityList(n)
})

//listar comunidades

// const getCommunities = async () => {

//   try {
//     const response = await http.get(`communities/`);
//     communities.value = response.data;

//   } catch (error) {
//     toast.add({
//         severity: 'danger',
//         summary: 'Upps!! algo ha fallado',
//         detail: error,
//         life: 3000
//     });
//   }
// }

// getCommunities()

function updateItems() {
   window.location.reload(); // intentar cambiar
  setTimeout(() => {
   // getCommunities()
  }, 300);
}

//currentCommunity
const isCurrent = (id)=> {
    return user?.current_community?.community_id === id
}

const sortedCommunities = computed(() => {
  return [...communities.value].sort((a, b) => {
    if (a.community_id === user?.current_community?.community_id) return -1 // Mover a al principio
    if (b.community_id === user?.current_community?.community_id) return 1  // Mover b al principio si b tiene el ID
    return 0 // Mantener el orden original
  })
})

const filteredCommunities = computed(() => {
  const query = search.value.toLowerCase();

  return sortedCommunities.value.filter(community => {
    return community.community_name.toLowerCase().includes(query)
  })
})

const setCurrent = (id) => {
    try {
        const response = http.put(`members/me/update/`, {
            current_community: id
        })
        toast.add({
            severity: 'success',
            summary: 'OK',
            detail: 'Has cambiado de Comunidad',
            life: 3000
        });
        updateItems()
       // window.location.reload();
    } catch (error) {
        toast.add({
            severity: 'danger',
            summary: 'Upps!! algo ha fallado',
            detail: error,
            life: 3000
        });
    }
}

const configCommunity = (id) => {
    route.push({ name: 'settings', params: { id:id } })
}
onMounted(() => {
  communities.value = user.available_communities
})

</script>

