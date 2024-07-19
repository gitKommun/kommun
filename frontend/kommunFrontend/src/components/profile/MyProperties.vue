<template>
    <Fieldset legend="Mis propiedades">
        <template v-if="properties.length">
            //Listado de propiedades
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
    </Fieldset>
</template>
<script setup>
import { ref } from 'vue';

import EmptyTask from "/src/components/emptys/EmptyTask.vue"

    defineOptions({
        name: 'MyProperties',
    })

//Variables
    const properties = ref([])
</script>