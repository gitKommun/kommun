<template>
  <div class="h-full w-full overflow-y-scroll px-4">
    <Tabs value="0">
      <TabList>
        <Tab as="div" value="0">
          <span class="flex items-center gap-x-2">
           Mis datos
            </span>
        </Tab>
        <Tab as="div" value="1">
          Mi Plan
        </Tab>
      </TabList>
      <TabPanels>
        <TabPanel value="0">
          <Content>
            <PersonalData/>
          </Content>
        </TabPanel>
        <TabPanel value="1">
          Billing data
        </TabPanel>
      </TabPanels>
    </Tabs>
  </div>  
</template>
<script setup>
import { ref , shallowRef} from 'vue'
import Main from '/src/layouts/Main.vue';
import { useUserStore } from '/src/stores/useUserStore.js';
import IconHome from "/src/components/icons/IconHome.vue"

import { useHttp } from '/src/composables/useHttp.js'; 
import PersonalData from '/src/components/profile/PersonalData.vue'

import Content from '/src/components//Content.vue'

const { user } = useUserStore();

defineOptions({
  name: 'account',
  layout: Main
})
const title = ref('Mi perfil')

const form = ref({
    name: user.name,
    surname: user.surnames,
    email: user.email,
    phone: user.phoneNumber,
    identificationNumber: user.documentID ?user.documentID : '',
    identificationType: user.documentType ?user.documentType : '',
    allowSharing:user.contactIsPublic   
})


</script>

