<template>
  <div class="flex-1 min-h-0 overflow-y-scroll  px-4">
    <Content>
      <div class="flex flex-col gap-y-4 pt-8">
        <PersonalData/>
        <MyProperties/>
      </div>
    </Content>
    <ConfirmDialog></ConfirmDialog>
    <Toast />
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
import { useUserStore } from '/src/stores/useUserStore.js';


import { useHttp } from '/src/composables/useHttp.js'; 
import PersonalData from '/src/components/profile/PersonalData.vue'
import MyProperties from '/src/components/profile/MyProperties.vue'

import Content from '/src/components/Content.vue'

const { user } = useUserStore();

defineOptions({
  name: 'account',
  layout: Main
})



</script>

