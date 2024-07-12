<template>
    <div class="">
         <vs-button color="dark" @click="showCreateSurvey =!showCreateSurvey">
                <IconPlus class="mr-2"/>
              Nueva consulta
        </vs-button>
        <vs-dialog v-model="showCreateSurvey" overlay-blur>
            <template #header>
              <span>Crear nueva consulta</span>
            </template>
            <div class="">
              <div class="flex ">
                    <vs-input 
                        v-model="form.title" 
                        placeholder="Pregunta" 
                        label-float 
                        block/>
                </div>
                <div class="">
                    <vs-input 
                        v-model="form.description" 
                        placeholder="Descripción" 
                        label-float 
                        block/>
                </div>
                <div class="">
                    <vs-select v-model="form.type" label="Tipo de pregunta" block label-float>
                        <vs-option label="única" value="unique"> Única</vs-option>
                        <vs-option label="multiple" value="owner"> Multiple </vs-option>
                        <vs-option label="ranking" value="tenant"> Ranking</vs-option>
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
import { ref, watch} from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';

import IconPlus from "/src/components/icons/IconPlus.vue";
import IconCircleCheck from "/src/components/icons/IconCircleCheck.vue";
import { VsNotification } from 'vuesax-alpha'

defineOptions({
    name: 'AddNewSurvey',
})

//variables
const showCreateSurvey = ref(false);
const form = ref({
    title: '',
    description: '',
    type:null,
})
</script>