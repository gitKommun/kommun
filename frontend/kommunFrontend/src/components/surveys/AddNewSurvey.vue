<template>
  <div class="">
    <Button
      @click="showCreateSurvey = !showCreateSurvey"
      severity="contrast"
      raised
    >
      <IconPlus />
      <span class="hidden md:flex">Nueva votación</span>
    </Button>
    <Dialog
      v-model:visible="showCreateSurvey"
      modal
      header="Crear nueva consulta"
      class="w-128"
    >
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
              variant="filled"
              class="w-full mb-4"
            />
            <Textarea
              v-model="form.description"
              placeholder="Descripción"
              variant="filled"
              class="w-full"
            />
            <div
              class="flex justify-between border-t border-slate-200 mt-3 flex-col"
            >
              <div class="text-xs text-slate-500 uppercase py-3">
                Opciones de respuesta
              </div>
              <div
                v-for="(option, index) in form.options"
                :key="index"
                class="flex items-center w-full gap-x-2 py-1 mb-2"
              >
                <InputText
                  v-model="form.options[index]"
                  :placeholder="'Opción ' + (index + 1)"
                  variant="filled"
                  class="w-full"
                />
                <Button
                  severity="danger"
                  text
                  class="min-w-10"
                  @click="removeOption(index)"
                >
                  <IconTrash />
                </Button>
              </div>
              <Button text @click="addOption()">
                <IconPlus />
                Nueva opción
              </Button>
            </div>

            <div class="flex justify-end gap-x-4 pt-4">
              <Button
                severity="secondary"
                text
                @click="showCreateSurvey = !showCreateSurvey"
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
              <Select
                v-model="form.vote_type"
                :options="answerTypes"
                optionLabel="label"
                optionValue="value"
                placeholder="Respuesta..."
                class="w-full mb-4"
                variant="filled"
              />
              <div class="flex gap-x-3">
                <DatePicker
                  v-model="form.start_date"
                  dateFormat="dd/mm/yy"
                  :manualInput="false"
                  variant="filled"
                  placeholder="Fecha de inicio"
                  class="w-full"
                />
                <DatePicker
                  v-model="form.end_date"
                  dateFormat="dd/mm/yy"
                  :manualInput="false"
                  variant="filled"
                  placeholder="Fecha de fin"
                  class="w-full"
                />
              </div>

              <div class="flex items-center mt-6">
                <span class="min-w-10">
                  <ToggleSwitch v-model="enableAllAudience" />
                </span>
                <span class="ml-3">
                  Enviar a todos los miembros de la comunidad
                </span>
              </div>
              <transition
                enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                enter-class="opacity-0"
                enter-to-class="opacity-100"
                leave-class="opacity-100"
                leave-to-class="opacity-0"
              >
                <div v-if="!enableAllAudience" class="mt-4">
                  <UserSelectorMultiple
                    @update:selected="
                      (owners) => (form.eligible_voters = owners)
                    "
                  />
                </div>
              </transition>
            </div>

            <div class="flex justify-end gap-x-4 pt-4">
              <Button
                severity="secondary"
                outlined
                @click="activateCallback('1')"
              >
                Atras
              </Button>
              <Button severity="contrast" @click="createSurvey()">
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
import { ref, watch } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

import IconPlus from "/src/components/icons/IconPlus.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";
import UserSelectorMultiple from "/src/components/UserSelectorMultiple.vue";

defineOptions({
  name: "AddNewSurvey",
});

//variables
const showCreateSurvey = ref(false);
const form = ref({
  title: "",
  description: "",
  vote_type: null,
  options: [""],
  end_date: null,
  start_date: null,
  eligible_voters: [],
});

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const emit = defineEmits(["update:surveys"]);

const enableAllAudience = ref(true);

const answerTypes = ref([
  { label: "Única", value: "simple" },
  { label: "Multiple", value: "multiple_choice" },
  // {label:'Ranking',value:'ranking'}
]);

const addOption = () => {
  form.value.options.push("");
};

const removeOption = (index) => {
  if (form.value.options.length > 1) {
    form.value.options.splice(index, 1);
  }
};

const createSurvey = async () => {

  try {
    await http.post(`votes/${user?.current_community?.community_id}/create/`, {
      title: form.value.title,
      description: form.value.description,
      vote_type: form.value.vote_type,
      options: form.value.options,
      end_date: form.value.end_date,
      start_date: form.value.start_date,
      eligible_voters:
        form.value.eligible_voters.length > 0
          ? form.value.eligible_voters.map((owner) => owner.person_id)
          : [],
    });
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "Votacion creada con exito",
      life: 3000,
    });
    emit("update:surveys", true);
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
  form.value = {
    title: "",
    description: "",
    vote_type: null,
    options: [""],
    end_date: null,
    start_date: null,
    eligible_voters: [],
  };
  showCreateSurvey.value = false;
};
</script>
