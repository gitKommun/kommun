<template>
    <div class="h-screen w-screen flex justify-center items-center">
        
        <div class="bg-white w-96 rounded-2xl shadow-2xl p-4">
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
                    block/>
                <vs-input
                    v-model="password"
                    type="password"
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
                <RouterLink :to="{name:'members'}">
                    <vs-button color="dark">Sign in</vs-button>
                </RouterLink>
                
            </div>
            
            
            
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import IconArrowBack from "/src/components/icons/IconArrowBack.vue"
import Authentication from '/src/layouts/Authentication.vue';
    defineOptions({
        name: 'login',
        layout:Authentication
    });
    const email = ref('');
    const password = ref('');
    
</script>