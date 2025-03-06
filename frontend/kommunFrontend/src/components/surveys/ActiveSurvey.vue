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
        <!-- Si he delegado mi voto -->
        <template v-if="isMyDirectSurvey && myDelegationStatus.isDelegated">
          <CustomTag>
            Delegado a: <span class="ml-1 font-bold">{{ myDelegationStatus.delegatedTo.fullName }}</span>
          </CustomTag>
        </template>

        <!-- Si soy delegado -->
        <template v-if="amIDelegated && delegator">
          <CustomTag color="purple">
            Delegado por: <span class="ml-1 font-bold">{{ delegator.fullName }}</span>
          </CustomTag>
        </template>
      </div>
      <div class="flex gap-2">
        <!-- Si soy usuario directo y no he delegado -->
        <template v-if="isMyDirectSurvey && !myDelegationStatus.isDelegated">
          <Button 
            severity="contrast" 
            outlined 
            size="small"
            @click="showDelegate = true"
          >
            Delegar
          </Button>
          <Button 
            severity="contrast" 
            size="small"
            @click="showSurvey = true"
          >
            Votar
          </Button>
        </template>

        <!-- Si he delegado mi voto -->
        <template v-if="isMyDirectSurvey && myDelegationStatus.isDelegated">
          <Button 
            severity="danger" 
            outlined 
            size="small"
            :disabled="!myDelegationStatus.canCancelDelegation"
            @click="cancelDelegation"
          >
            Anular delegación
          </Button>
        </template>

        <!-- Si soy delegado -->
        <template v-if="amIDelegated">
          <Button 
            severity="contrast" 
            size="small"
            @click="showSurvey = true"
          >
            Votar como delegado
          </Button>
        </template>
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
          <Button @click="vote()" severity="contrast" class="w-full"
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
        <UserSelector @update:selected="(owner) => selectionDelegate(owner)" :exclude="user?.current_community?.community_person_id" />
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
import CustomTag from "/src/components/CustomTag.vue";
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
    required: true
  },
});
//utils
const http = useHttp();
const toast = useToast();
const { user } = useUserStore();
const emit = defineEmits(["update:surveys"]);

// Estados
const showSurvey = ref(false);
const showDelegate = ref(false);
const selectedOption = ref(null);
const delegateTo = ref(null);

// Computed Properties
// 1. Verificar si soy el usuario de esta survey
const isMyDirectSurvey = computed(() => {
  return props.survey.users.person_community_id === user.current_community.community_person_id;
});

// 2. Verificar si soy el delegado
const amIDelegated = computed(() => {
  return props.survey.users.delegate_to?.person_community_id === user.current_community.community_person_id;
});

// 3. Estado de delegación
const myDelegationStatus = computed(() => {
  if (!isMyDirectSurvey.value) return { isDelegated: false, delegatedTo: null, canCancelDelegation: false };
  
  return {
    isDelegated: Boolean(props.survey.users.delegate_to),
    delegatedTo: props.survey.users.delegate_to,
    canCancelDelegation: props.survey.users.answer.length === 0
  };
});

// 4. Información del delegador (si soy delegado)
const delegator = computed(() => {
  if (!amIDelegated.value) return null;
  return {
    person_community_id: props.survey.users.person_community_id,
    fullName: props.survey.users.fullName
  };
});

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
    emit("update:surveys", true);
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Ocurrió un error al procesar tu voto',
      life: 3000
    });
  }
};

const cancelDelegation = async () => {
  try {
    await http.post(`votes/${user?.current_community?.community_id}/polls/${props.survey.vote_id}/vote/`, {
      person_id: user?.current_community?.community_person_id,
      delegated_to: null,
    });

    toast.add({
      severity: 'success',
      summary: 'Éxito',
      detail: 'Delegación anulada correctamente',
      life: 3000
    });

    emit("update:surveys", true);
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Ocurrió un error al anular la delegación',
      life: 3000
    });
  }
};

const selectionDelegate = (delegate) => {
  delegateTo.value = delegate.person_id;
};

console.log('delegatedByMe:', props.survey.users);
console.log('myDelegatedTo:', myDelegationStatus.delegatedTo);
</script>
