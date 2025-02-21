<template>
    <Fieldset legend="Mis propiedades">
        <template v-if="myProperties.length">
            <div class="flex flex-col gap-4">
                <PropertyCard v-for="property in myProperties" :key="property.id" :property="property" />
            </div>
        </template>
        <template v-else>
            <div  class="w-full flex flex-col items-center justify-center py-16">
                  <EmptyTask class="scale-75"/>
                  <span class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300">
                      Actualmente no hay propiedades
                  </span>
                  <span class="text-sm text-slate-500 max-w-80 text-center mb-3">
                      Actualmente aun no tienes propiedades vinculadas en está comunidad
                  </span>
                </div>
        </template>
        <toast />
    </Fieldset>
</template>
<script setup>
import { ref, computed } from 'vue';
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

import EmptyTask from "/src/components/emptys/EmptyTask.vue"
import PropertyCard from "/src/components/profile/PropertyCard.vue"

    defineOptions({
        name: 'MyProperties',
    })
//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
//Variables
const properties = ref([])


    const getProperties = async () => {
  try {
    const response = await http.get(
      `properties/${user?.current_community?.community_id}/`
    );
    properties.value = response.data;
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
};

getProperties();

//funcion computada para devolver las porperties que tengan el owner_id igual al id del usuario
const myProperties = computed(() => {
    return properties.value.filter(property => property.owner?.person_id === user.current_community.community_person_id);
});



</script>