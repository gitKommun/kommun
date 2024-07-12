<template>
  <div class="h-full w-full">
    <div class="pl-4 md:pl-16 py-6 flex">
      <div class="w-full text-slate-950 text-3xl font-bold truncate flex flex-col">
          {{title}}
          <span class="text-sm text-slate-500 font-medium">{{ user.communities[0]?.community_name }}</span>
      </div>
      <div class="w-full p-4 flex justify-end">
          <AddNewSurvey  @update:items="updateItems" class="h-auto"/>
      </div>
    </div>
    <div class="w-full flex justify-center px-4 flex-1 min-h-0 overflow-y-scroll">
      <div class="w-full max-w-4xl  flex flex-col">
        content
      </div>
    </div>
  </div>  
</template>
<script setup>
import { ref } from 'vue'
import { useUserStore } from '/src/stores/useUserStore.js';
import Main from '/src/layouts/Main.vue';
import AddNewSurvey from '/src/components/surveys/AddNewSurvey.vue'
defineOptions({
  name: 'surveys',
  layout: Main
})

//variables
const title = ref('Votaciones')

//user store
const { user } = useUserStore();
</script>

