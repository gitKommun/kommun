<template>
    <div class="h-screen w-screen flex justify-center items-center">
        
        <div 
            class="bg-white w-96 rounded-2xl shadow-2xl p-4"
        >
            <div class="">
                <RouterLink to="/">
                    <vs-button color="dark" type="transparent" size="small"><IconArrowBack class="scale-75 mr-1"/> back</vs-button>
                </RouterLink>
            </div>

            <div class="w-full flex justify-center">
                <img alt="Kommun logo" class="h-24" src="@/assets/iso_kommun.svg"  />
            </div>

            <div class="flex flex-col gap-y-2 px-2">
                <vs-input 
                    v-model="email" 
                    placeholder="User email" 
                    label-float 
                    block
                />

                <vs-input
                    v-model="password"
                    type="text"
                    placeholder="Password"
                    label-float 
                    block
                />
            </div>

            <div class="flex justify-center items-center mt-2">
                <RouterLink :to="{name:'recovery'}">
                    <span class="text-xs text-cyan-500  hover:underline transition-all duration-300">forget password</span>
                </RouterLink>

                <span class="text-slate-500 text-xs mx-[4px]">or</span>

                <RouterLink :to="{name:'register'}">
                    <span class="text-xs text-cyan-500  hover:underline transition-all duration-300">create account</span>
                </RouterLink>
            </div>

            <div class="flex justify-center mt-4">
                <div class="flex justify-center mt-4">
                    <vs-button color="dark" @click="login" :loading="loginLoading">Sign in</vs-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import IconArrowBack from "/src/components/icons/IconArrowBack.vue"
import Authentication from '/src/layouts/Authentication.vue';
import { VsNotification } from 'vuesax-alpha'
import { setCookie } from '/src/utils/cookies.js';
import http from '/src/http.js'; 

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

// login
const login = async () => {
    loginLoading.value = true;

    try {
        console.log('Realizando solicitud POST a la API...');
        const response = await http.post(`members/login/`, {
            email: email.value,
            password: password.value,
        });

        //hacer llamada a /me
        loginLoading.value = false;

        //   Guardar en pinia usuario y token
        //redirecionar a home
        console.log('user--->', response);
        
        const { csrftoken, user } = response.data;
        console.log('token--->', csrftoken);
        console.log('user--->', user);

        setCookie('csrftoken', csrftoken, 30);
        setCookie('user', JSON.stringify(user), 30);

        router.push({ name: 'properties' });

    } catch (error) {
        console.error('Error en la solicitud POST:', error);
        // Manejar el error de autenticación
        VsNotification({
            position: 'top-right',
            color: 'danger',
            title: 'Error de autenticación',
            content: error,
        });

        loginLoading.value = false;
    }
}
</script>

