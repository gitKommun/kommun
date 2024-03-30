
<template>
    <div class="h-screen w-screen bg-gradient-to-tr from-indigo-400 via-blue-300 to-teal-300  flex justify-center items-center">
        
        <div class="bg-white w-96 rounded-2xl shadow-2xl p-4">
            <div class="flex justify-center mb-4">
                <img alt="Kommun logo" class="h-12 -ml-2" src="@/assets/logo_kommun.svg"  />
                
            </div>
            <div class="text-slate-500 text-sm px-4">
                <p>Introduce el email con el que te registraste, te mandaremos los pasos para recuperar tu contraseña</p>
            </div>

            <div class="flex flex-col gap-y-2 px-2">
                <vs-input 
                    v-model="email" 
                    placeholder="User email" 
                    label-float 
                    block/>
            </div>
            <div class="flex justify-between items-center mt-4">
                <RouterLink to="/">
                    <vs-button color="dark" type="transparent"> <IconArrowBack class="mr-1 "/> Back to home</vs-button>
                </RouterLink>
                <vs-button color="dark">Send</vs-button>
            </div>       
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import IconArrowBack from "/src/components/icons/IconArrowBack.vue"

    defineOptions({
        name: 'recovery',
    });
    const email = ref('');

    
</script>