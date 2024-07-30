<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex ">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.current_community?.community_name }}</span>
      </div>
      <div class="w-full p-4 flex justify-end">
        <AddNewCommunity @update:communities="updateItems" class="h-auto"/>  
      </div>
    </div>
    <!-- search and view -->
    <div v-if="communities.length" class="flex items-center justify-between py-4">
    
      <SelectButton v-model="toggleView" :options="toggleViewOptions" optionLabel="value" >
          <template #option="slotProps">
              <IconGrid v-if="slotProps.option === 'card'"/>
              <IconTable v-else/>
          </template>
      </SelectButton>
    </div>
    <!-- search and view -->
    
     <div class=" w-full flex justify-center px-4 flex-1 min-h-0 overflow-y-scroll">
       <div class="w-full max-w-4xl  flex flex-col">
          <!-- cards -->
          <div 
           v-if="toggleView === 'card'"
          class="w-full flex flex-wrap gap-3 pb-4"
          key="cards">
            <CommunityItem
              v-for ="community in communities"
              :key="community.community_id"
              :community="community"
              @update:community="updateItems"
            />
          </div>
          <!-- cards-->
          <!-- table -->
           <div 
            v-else
            class="w-full"
            key="table">
            <DataTable :value="communities" class="text-sm">
              <column header="Comunidad" >
                <template #body="slotProps">
                  <CustomTag
                    v-if="isCurrent(slotProps.data.IDcommunity)"
                    :solid="true"
                    :color="'green'"
                    >
                    Actual
                    </CustomTag>
                  <span :class="isCurrent(slotProps.data.IDcommunity)?'ml-2':''">{{slotProps.data.nameCommunity}}</span>
                </template>
              </column>
              <column header="Dirección" field="address"></column>

            </DataTable>
           </div>
          <!-- table -->
       </div>
     </div>


  </div>  
</template>
<script setup>
import { ref, shallowRef } from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';

import Main from '/src/layouts/Main.vue';
import AddNewCommunity from '/src/components/communities/AddNewCommunity.vue'
import CommunityItem from '/src/components/communities/CommunityItem.vue'
import IconTable from '@/components/icons/IconTable.vue'
import IconGrid from '@/components/icons/IconGrid.vue'
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

const communities = ref([]);
const toggleView = ref('card');
const toggleViewOptions = ref(['card','table'])

//listar comunidades

const getCommunities = async () => {

  try {
    const response = await http.get(`communities/`);
    communities.value = response.data;

  } catch (error) {
    toast.add({
        severity: 'danger',
        summary: 'Upps!! algo ha fallado',
        detail: error,
        life: 3000
    });
  }
}

getCommunities()

function updateItems() {
  setTimeout(() => {
    getCommunities()
  }, 300);
}

//currentCommunity
const isCurrent = (id)=> {
    return user?.current_community?.community_id === id
}


</script>

