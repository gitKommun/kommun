<template>
  <div
    class="flex flex-col items-start border border-purple-100 p-3 bg-purple-50 rounded-2xl gap-x-3 mb-3 w-full relative transition-all duration-300"
  >
    <div class="text-slate-500 text-xs">
      <span>HASTA: {{ formatDate(survey.start_date) }}</span>
    </div>
    <div class="w-full flex font-bold mb-2">
      {{ survey.title }}
    </div>
    <div class="w-full flex justify-between items-center">
      <div class="text-slate-500 text-sm">
        <!-- soy delegado -->
        <template v-if="isDelegated">
          <CustomAvatar :name="'juan Palomo'" size="small" />
          <span class="text-sm text-slate-500"> Juan Palomo </span>
          <span>te ha delegado su voto</span>
        </template>
        <!-- me han delegado -->
        <template v-if="iAmDelegated">
          <span class="mr-1">Voto delegado a</span>
          <CustomAvatar :name="'juan Palomo'" size="small" />
          <span class="text-sm text-slate-500"> Juan Palomo </span>
        </template>
      </div>
      <div class="flex gap-2">
        <Button 
        v-if="!isDelegated" 
        severity="contrast" 
        outlined 
        size="small"
        @click="showDelegate = !showDelegate"
        >Delegar</Button
        >
        <Button @click="showSurvey = true" severity="contrast" size="small"
          >Votar</Button
        >
      </div>
    </div>
    <Dialog v-model:visible="showSurvey" modal header="Votación" class="w-128">
      <div>
        <div class="text-lg font-bold">
          {{ survey.title }}
        </div>
        <div class="text-sm text-slate-500">
          {{ survey.description }}
        </div>
        <div class="py-3 flex flex-col gap-2">
          <div
            v-for="(el, index) in survey.options"
            :key="index"
            @click="selectOption(el)"
            class="border hover:bg-slate-100 rounded-lg p-3 w-full transition-all duration-300"
            :class="
              selectedOption?.option_id === el.option_id
                ? 'border-green-500 bg-green-50 text-green-500 font-semibold'
                : 'border-slate-200 '
            "
          >
            {{ el.option_text }}
          </div>
        </div>
        <div class="flex justify-end">
          <Button @click="vote" severity="contrast" class="w-full"
            >Votar</Button
          >
        </div>
      </div>
    </Dialog>
    <Dialog
      v-model:visible="showDelegate"
      modal
      header="Delegar voto"
      class="w-96"
    >
      <div class="mb-4">
        <UserSelector @update:selected="(owner) => selectionDelegate(owner)" />
      </div>
      <div class="flex justify-end gap-x-4">
        <Button
          text
          severity="secondary"
          @click="showDelegate = !showDelegate"
          label="Cancelar"
        />
        <Button severity="contrast" @click="vote()" label="Delegar" />
      </div>
    </Dialog>
  </div>
</template>
<script setup>
import { ref, computed, toRaw } from "vue";
import CustomAvatar from "/src/components/CustomAvatar.vue";
import UserSelector from "/src/components/UserSelector.vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useToast } from "primevue/usetoast";
import { useUserStore } from "/src/stores/useUserStore.js";
import { formatDate } from "@/utils/dateUtils";

defineOptions({
  name: "ActiveSurvey",
});

const props = defineProps({
  survey: {
    type: Object,
  },
});
//utils
const http = useHttp();
const toast = useToast();
const { user } = useUserStore();

//variables
const isDelegated = ref(false);
const iAmDelegated = ref(false);
const showSurvey = ref(false);
const showDelegate = ref(false);
const selectedOption = ref(null);
const delegateTo = ref(null);

const selectOption = (option) => {
  selectedOption.value = option;
};

const vote = async () => {
  try {
   
    await http.post(`votes/${user?.current_community?.community_id}/polls/${props.survey.vote_id}/vote/`, {
      person_id: user?.current_community?.community_person_id,
      option_ids: selectedOption.value?.option_id,
      delegated_to: delegateTo.value,
    });

    toast.add({
      severity: 'success',
      summary: 'Éxito',
      detail: delegateTo.value ? 'Voto delegado correctamente' : 'Voto registrado correctamente',
      life: 3000
    });

    showSurvey.value = false;
    showDelegate.value = false;
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Ocurrió un error al procesar tu voto',
      life: 3000
    });
    console.error('Error al votar:', error);
  }
};
//saber si me han delegado el voto
const delegatedToMe = computed(() => {
  return props.survey.delegated_to === user.currentCommunity.community_person_id;
});
//saber si yo he delegado el voto
const delegatedByMe = computed(() => {
  return props.survey.delegated_to !== null;
});

const selectionDelegate = (delegate) => {
  console.log(delegate);
  delegateTo.value = delegate.person_id;
};
</script>
