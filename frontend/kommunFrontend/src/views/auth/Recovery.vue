
<template>
    <div class="h-screen w-screen  flex justify-center items-center">
        
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
                <vs-button @click="openNotification" color="dark">Send</vs-button>
            </div>       
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import IconArrowBack from "/src/components/icons/IconArrowBack.vue"
import { VsNotification } from 'vuesax-alpha'
import Authentication from '/src/layouts/Authentication.vue';

    defineOptions({
        name: 'recovery',
        layout:Authentication
    });
    const email = ref('');
    const openNotification = () => {
        VsNotification({
            position: 'top-right',
        color:'success',
        title: 'Te hemos enviado un mail',
        content:
        'Revisa tu bandeja de correo y sigue las innstrucciones para recuperar tu acceso',
    })
}
    
</script>