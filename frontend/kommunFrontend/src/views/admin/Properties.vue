<template>
  <div class="h-full w-full flex flex-col">
    <div class="pl-4 md:pl-16 py-6 flex sticky top-0  backdrop-blur z-10">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">Comunidad : {{ user.current_community?.community_name }}</span>
      </div>
      <div class=" p-4 flex justify-end">
        <!-- <Button severity="contrast" raised  class="inline flex-none">
          <IconPlus/>
          Añadir propiedad
        </Button> -->
      </div>
    </div>
    
    <div class="px-4 overflow-y-scroll min-h-0 flex-1">
        <DataTable 
            :value="properties" 
            paginator 
            scrollable
            scrollHeight="700px"
            :rows="20" 
            :rowsPerPageOptions="[20, 40, 60, 100]"
            tableStyle="min-width: 50rem" 
            class="text-xs">
            <Column field="address_complete" sortable header="Dirección"></Column>
            <Column field="surface_area" sortable header="Sup. m&sup2"></Column>
            <Column field="participation_coefficient" sortable header="Participación"></Column>
            <Column field="usage" sortable header="Uso">
              <template #body="slotProps">
                <CustomTag
                        :color="usageTagColor(slotProps.data.usage)"
                        >
                        {{slotProps.data.usage}}
                </CustomTag>
              </template>
            </Column>
            <Column field="staircase" sortable header="Esc"></Column>
            <Column field="floor" sortable header="Piso"></Column>
            <Column field="door" sortable header="Pta"></Column>
            <Column  header="Propietario">
              <template #body="slotProps">
                <UserSelector  @update:selected="(owner) => updateOwner(owner, slotProps.data)"/>
              </template>
            </Column>
        </DataTable>
    </div>
    <toast/>
  </div>  
</template>
<script setup>
import { ref , toRef, shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
import IconPlus from "/src/components/icons/IconPlus.vue";
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';
import CustomTag from '/src/components/CustomTag.vue'
import UserSelector from '/src/components/UserSelector.vue'
import { USAGES } from '/src/constants/colors.js';

defineOptions({
  name: 'properties',
  layout: Main
})
const title = ref('Propiedades')

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const route = useRouter();

//variables
const properties = ref([]);
const updating = ref(null);

const getProperties = async () => {
  try {
      const response = await http.get(`properties/${user?.current_community?.community_id}/`);
      properties.value = response.data
      
    } catch (error) {
     toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
}

getProperties()

const usageTagColor = (usage) => {
  return USAGES[usage];
}

const updateOwner =  (owner, data) => {
  console.log('owner :>> ', owner, data);
  const { person_id } = owner;
  const { property_id } = data;

  console.log('des', person_id, property_id);
  try {
    http.post(`properties/${user?.current_community?.community_id}/property-relationship/create/`, {
      property_id: property_id,
      person_id: person_id,
      type:'owner'
      });  
      toast.add({
            severity: 'success',
            summary: 'Ok',
            detail: 'Prpietario vinculado con exito',
            life: 3000
        });    
    } catch (error) {
     toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
}

</script>

