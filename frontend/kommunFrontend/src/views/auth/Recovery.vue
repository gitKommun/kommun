
<template>
    <div class="h-screen w-screen  flex justify-center items-center">
        
        <div class="bg-white w-96 rounded-2xl shadow-2xl p-4">
            <div class="flex justify-center mb-4">
                <img alt="Kommun logo" class="h-12 -ml-2" src="@/assets/logo_kommun.svg"  />
                
            </div>
            <div class="text-slate-500 text-sm px-4">
                <p>Introduce el email con el que te registraste, te mandaremos los pasos para recuperar tu contraseña</p>
            </div>

            <div class="flex flex-col gap-y-2 px-2 py-4">
                <InputText
                    v-model="email" 
                    placeholder="User email" 
                    class="w-full"
                    variant="filled"/>
            </div>
            <div class="flex justify-between items-center mt-4">
                <RouterLink to="/">
                    <Button size="small" text><IconArrowBack class="mr-1 "/>Back to home</Button>
                </RouterLink>
                <Button @click="openNotification" severity="contrast" label="Enviar" class="min-w-32" raised/>
            </div>       
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import IconArrowBack from "/src/components/icons/IconArrowBack.vue"
import Authentication from '/src/layouts/Authentication.vue';

    defineOptions({
        name: 'recovery',
        layout:Authentication
    });

    //use toast
    const toast = useToast();

    //Variables
    const email = ref('');


    
</script>