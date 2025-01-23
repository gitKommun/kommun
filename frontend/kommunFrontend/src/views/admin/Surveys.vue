<template>
  <div class="h-full w-full">
    <div class="w-full p-4 flex justify-end">
          <AddNewSurvey  @update:items="updateItems" class="h-auto"/>
    </div>
    <div class="w-full flex justify-center px-4 flex-1 min-h-0 overflow-y-scroll">
      <div class="w-full max-w-4xl  flex flex-col">
        <div class="">
          <h2 class="font-bold text-slate-950">Votaciones activas</h2>
          <div class="flex py-3">
            <div class="border border-slate-200 rounded-2xl p-3 min-w-80">
                <p class="font-bold">Titulos de la votacion</p>
                <span class="text-sm text-slate-500">Periodo</span>
                <div class="flex items-center">
                  <div class="w-full">
                    <ProgressBar :value="(35*100)/68" style="height: 6px" :showValue="false"/>
                  </div>
                  <div class="flex justify-end min-w-12  text-xs text-slate-500">
                    35/68
                  </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>  
</template>
<script setup>
import { ref } from 'vue'
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';
import { useHttp } from '/src/composables/useHttp.js';

import Main from '/src/layouts/Main.vue';
import AddNewSurvey from '/src/components/surveys/AddNewSurvey.vue'

defineOptions({
  name: 'surveys',
  layout: Main
})

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const route = useRouter();

//variables
const surveys = ref([]);


const getSurveys = async () => {
  try {
      const response = await http.get(`properties/${user?.current_community?.community_id}/`);
      surveys.value = response.data
      
    } catch (error) {
     toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    }
}

getSurveys()

</script>

