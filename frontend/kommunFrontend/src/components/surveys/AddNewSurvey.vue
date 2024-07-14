<template>
    <div class="">

        <Button  @click="showCreateSurvey =!showCreateSurvey" severity="contrast" raised>
                <IconPlus class="mr-2"/>
              Nuevo
        </Button>
        <Dialog v-model:visible="showCreateSurvey" modal header="Crear nueva consulta" class="w-128">

            <Stepper value="1" linear class="basis-[50rem]">
                <StepList>
                    <Step value="1">Pregunta</Step>
                    <Step value="2">Configuración</Step>
                </StepList>
                <StepPanels>
                    <StepPanel v-slot="{ activateCallback }" value="1">
                        <InputText
                          v-model="form.title" 
                          placeholder="Pregunta" 
                          class="w-full mb-4"/>
                        <Textarea
                          v-model="form.description" 
                          placeholder="Descripción" 
                          class="w-full"/>
                        <div class="flex justify-between border-t border-slate-200 mt-3 flex-col">
                            <div class="text-xs text-slate-500 uppercase py-3">Opciones de respuesta</div>
                            <div v-for="(option, index) in form.options" :key="index" class="flex items-center w-full gap-x-2 py-1 mb-2">
                              <InputText v-model="form.options[index]"  :placeholder="'Opción ' + (index + 1)" class="w-full"/>
                              <Button 
                                severity="danger"
                                text 
                                class="min-w-10"
                                @click="removeOption(index)">
                                  <IconTrash/>
                              </Button>
                            </div>
                            <Button 
                              text
                              @click="addOption()"
                              >
                              <IconPlus/>
                              Nueva opción
                            </Button>
                        </div>

                        <div class="flex justify-end gap-x-4 pt-4">
                            <Button 
                              severity="secondary"
                              text
                              @click="showCreateSurvey =!showCreateSurvey"
                              >
                              Cancelar
                            </Button>
                            <Button 
                              severity="contrast"
                              outlined
                              @click="activateCallback('2')"
                  
                              >
                              Siguiente
                            </Button>
                        </div>
                    </StepPanel>
                    <StepPanel v-slot="{ activateCallback }" value="2">
                      <div class="w-full flex-col gap-y-2">
                        <Select v-model="form.type" :options="answerTypes" optionLabel="label" optionValue="value" placeholder="Respuesta..." class="w-full"/>
                        <DatePicker v-model="form.dates" selectionMode="range" :manualInput="false" placeholder="Habilitar desde... hasta " class="w-full"/>
                        <div class="flex items-center mt-6">
                                <span class="min-w-10">
                                    <ToggleSwitch v-model="enableAllAudience" />
                                </span>
                            <span class="ml-3"> Enviar a todos los miembros de la comunidad </span>
                        </div> 
                      </div>
                        
                        <div class="flex justify-end gap-x-4 pt-4">
                            <Button 
                              severity="secondary"
                              outlined
                              @click="activateCallback('1')"
                              >
                              Atras
                            </Button>
                            <Button 
                              severity="contrast"
                              @click="createSurvey()"
                  
                              >
                              Crear
                            </Button>
                        </div>
                    </StepPanel>
                    
                </StepPanels>
            </Stepper>              
          </Dialog> 
    </div>
    
</template>
<script setup>
import { ref, watch} from 'vue'
import { useHttp } from '/src/composables/useHttp.js'; 
import { useUserStore } from '/src/stores/useUserStore.js';

import IconPlus from "/src/components/icons/IconPlus.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";


defineOptions({
    name: 'AddNewSurvey',
})

//variables
const showCreateSurvey = ref(false);
const form = ref({
    title: '',
    description: '',
    type: null,
    options: [],
    dates: null,
    eligible_voters:[]
})

const  enableAllAudience = ref(true)

const answerTypes = ref([
    { label: 'Única', value: 'simple' },
    { label: 'Multiple', value: 'multiple_choice' },
    {label:'Ranking',value:'ranking'}
])

const addOption = () => {
  form.value.options.push('')
}

const removeOption = (index) => {
  if (form.value.options.length > 1) {
    form.value.options.splice(index, 1);
  }
};

const createSurvey = () => {
  console.log('survey',form)
}

</script>