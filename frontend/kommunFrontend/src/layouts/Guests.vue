<template>
    <div class="h-full w-full relative">
        <header class="absolute top-0 w-full text-slate-950">
            <div class="container mx-auto flex items-center justify-between py-2 px-6">
                <RouterLink to="/">
                    <img alt="Kommun logo" class="h-12" src="@/assets/logo_kommun.svg"  />
                </RouterLink>
                <div class="hidden md:flex items-center space-x-4">
                    <RouterLink :to="{name:'features'}">
                        <vs-button color="dark" type="transparent" >Features</vs-button>
                    </RouterLink>
                    <RouterLink :to="{name:'features'}">
                        <vs-button color="dark" type="transparent" >About</vs-button>
                    </RouterLink>
                    <RouterLink :to="{name:'features'}">
                        <vs-button color="dark" type="transparent" >Pricing</vs-button>
                    </RouterLink>
                    <RouterLink :to="{name:'features'}">
                        <vs-button color="dark" type="transparent" >Contact</vs-button>
                    </RouterLink>
                </div>
                <div class="flex items-center space-x-4">
                    <router-link :to="{name:'login'}">
                        <vs-button color="dark" type="border">Login</vs-button>
                    </router-link >
                    <router-link :to="{name:'register'}">
                        <vs-button color="dark">Registro</vs-button>
                    </router-link>
 
                </div>
                <div class="md:hidden flex items-center">
                    <button id="menu-toggle" class="text-gray-200 focus:outline-none">
                    <i class="fas fa-bars"></i>
                    </button>
                </div>
            </div>
        </header>
        <!-- <RouterView /> -->
        <Home/>
    </div>
</template>
<script setup>
import Home from "/src/views/Home.vue"
defineOptions({
    name: 'Guests',
        
    });

</script>