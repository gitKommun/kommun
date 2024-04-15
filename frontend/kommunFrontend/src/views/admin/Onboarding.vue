<template>
    <div class="h-screen w-screen  flex justify-center items-center">
        
        <div class="bg-white w-5/6 md:w-2/3 rounded-2xl shadow-2xl overflow-hidden flex flex-col md:flex-row">
            <div class="bg-slate-50 flex items-center w-full md:w-1/3">
                <img alt="Kommun logo" class="w-full h-auto" src="@/assets/construction.png"  />
            </div>
            <div class="p-8 w-full md:w-2/3">
                <div class="w-full text-center font-bold text-2xl text-slate-950 mb-4">¡Vamos a contruir una comunidad!</div>
                <div class="py-4 gap-y-2">
                    <div class="">
                        <vs-input v-model="form.name" placeholder="Nombre de la comunidad" label-float block/>
                    </div>
                    <div class="">
                        <vs-input v-model="form.address" placeholder="Dirección" label-float  block/>
                    </div>
                    <div class="flex gap-x-3 ">
                        <vs-input v-model="form.city" placeholder="Ciudad" label-float  block/>
                        <vs-input v-model="form.postalCode" placeholder="Código postal" label-float  block/>
                    </div>
                </div>
                <div class="w-full flex flex-end">
                    <vs-button color="dark">Crear mi comunidad</vs-button>
                </div>
            </div>
        </div>
    </div>

</template>
<script setup>
import { ref } from 'vue'
import Authentication from '/src/layouts/Authentication.vue';
defineOptions({
  name: 'onboarding',
  layout: Authentication
})
const form = ref({
    name: '',
    address: '',
    city:'',
    postalCode:'',
})
</script>
