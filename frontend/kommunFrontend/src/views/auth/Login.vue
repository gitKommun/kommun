<template>
    <div class="h-screen w-screen flex justify-center items-center">
        
        <div 
            class="bg-white w-96 rounded-2xl shadow-2xl p-4"
        >
            <div class="">
                <RouterLink to="/">
                    <Button size="small" text severity="contrast">
                        <IconArrowBack class="scale-75 mr-1"/> back
                    </Button>
                </RouterLink>
            </div>

            <div class="w-full flex justify-center mb-4">
                <img alt="Kommun logo" class="h-24" src="@/assets/iso_kommun.svg"  />
            </div>

            <div class="flex flex-col gap-y-8 px-2">
                <InputText 
                    v-model="email" 
                    placeholder="User email"
                    variant="filled" 
                />

                <Password
                    v-model="password" 
                    placeholder="Contraseña"
                    inputClass="w-full"
                    :feedback="false"
                    toggleMask
                    variant="filled"
                    fluid/>
            </div>

            <div class="flex justify-center items-center mt-2">
                <RouterLink :to="{name:'recovery'}">
                    <span class="text-xs text-indigo-500  hover:underline transition-all duration-300">forget password</span>
                </RouterLink>

                <span class="text-slate-500 text-xs mx-[4px]">or</span>

                <RouterLink :to="{name:'register'}">
                    <span class="text-xs text-indigo-500  hover:underline transition-all duration-300">create account</span>
                </RouterLink>
            </div>

            <div class="flex justify-center mt-4">
                <div class="flex justify-center mt-4">
                    <Button  @click="login" :loading="loginLoading" severity="contrast" label="Sign in" raised class="w-full"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';

import IconArrowBack from "/src/components/icons/IconArrowBack.vue"
import Authentication from '/src/layouts/Authentication.vue';
import { setCookie } from '/src/utils/cookies.js';
import { useHttp } from '/src/composables/useHttp.js';


const email = ref('');
const password = ref('');
const loginLoading = ref(false);


// options
defineOptions({
    name: 'login',
    layout:Authentication
});

// router
const router = useRouter();

//instancia API
const http = useHttp();

//use toast
const toast = useToast();

// login
const login = async () => {
    loginLoading.value = true;

    try {
        const response = await http.post(`members/login/`, {
            email: email.value,
            password: password.value,
        });
        
        const { csrftoken, sessionid } = response.data;

        setCookie('csrftoken', csrftoken, 30);
        setCookie('sessionid', sessionid, 30);

        router.push({ name: 'properties' });
    } catch (error) {

        // Manejar el error de autenticación
        toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });

        loginLoading.value = false;
    }
}
</script>

