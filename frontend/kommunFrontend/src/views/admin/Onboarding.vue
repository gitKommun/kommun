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
                        <InputText  v-model="form.name" placeholder="Nombre de la comunidad" class="w-full" variant="filled"/>
                    </div>
                    <div class="">
                        <InputText  v-model="form.address" placeholder="Dirección" class="w-full" variant="filled"/>
                    </div>
                    <div class="flex gap-x-3 ">
                        <InputText  v-model="form.city" placeholder="Ciudad" class="w-full" variant="filled"/>
                        <InputText  v-model="form.postalCode" placeholder="Código postal" class="w-full" variant="filled"/>
                    </div>
                </div>
                <div class="w-full flex flex-end">
                    <Button severity="contrast" label="Crear mi comunidad"/>
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
