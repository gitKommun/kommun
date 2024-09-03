<template>
    <div class="h-full w-full relative">
        <transition
            enter-from-class="-mt-16"
            enter-active-class="transitiona-all ease-in-out duration-150"
            move-class="transitiona-all bounce-transition duration-300"
            >
        <header v-if="AppearMenu" class="absolute top-0 w-full text-slate-950 backdrop-blur bg-black/30 z-20 ">
            <div class="container mx-auto flex items-center justify-between py-2 px-6">
                <RouterLink to="/">
                    <span class="flex items-center">
                        <img alt="Kommun logo" class="h-8" src="@/assets/lg_l.svg"  />
                        <span class="text-white font-bold ml-2">Kommun</span>
                    </span>
                </RouterLink>
                <!-- <div class="hidden md:flex items-center space-x-4">
                    <RouterLink to="/">
                        <Button label="Features" severity="secondary" text size="small" class="text-white"/>
                    </RouterLink>
                    <RouterLink to="/">
                        <Button label="About" severity="secondary" text size="small"/>
                    </RouterLink>
                    <RouterLink to="/">
                        <Button label="Pricing" severity="secondary" text size="small"/>
                    </RouterLink>
                    <RouterLink to="/">
                        <Button label="Contact" severity="secondary" text size="small"/>
                    </RouterLink>
                    
                </div> -->
                <div class="hidden md:flex items-center space-x-4">
                    <router-link :to="{name:'login'}">
                        <Button label="Login" severity="contrast" outlined size="small"/>
                    </router-link >
                    <router-link :to="{name:'register'}">
                        <Button 
                            label="Registro" 
                            severity="contrast" 
                            raised 
                            size="small"/>
                    </router-link>
 
                </div>
                <div class="md:hidden flex items-center">
                    <Button outlined severity="contrast" @click="showMobileMenu">    
                        <IconClose v-if="showMenu"/>
                        <IconMenu v-else/>
                    </Button>
                    
                </div>
            </div>
        </header>
        </transition>
        <transition
            enter-active-class="transition-all transition-slow ease-out overflow-hidden"
            leave-active-class="transition-all transition-slow ease-in overflow-hidden"
            enter-class="opacity-0"
            enter-to-class="opacity-100"
            leave-class="opacity-100"
            leave-to-class="opacity-0"
            mode="out-in"
            >
            <div v-if="showMenu" class="absolute top-0 mt-16 z-10 md:hidden items-center justify-between flex w-full lg:flex lg:w-auto lg:order-1 bg-white rounded-2xl shadow-xl">
                <div class="flex flex-col mt-4 font-medium w-full lg:flex-row lg:space-x-8 lg:mt-0 p-4">
                    <RouterLink :to="{name:'features'}">
                        <Button label="Features" severity="secondary" text/>
                    </RouterLink>
                    <RouterLink :to="{name:'features'}">
                        <Button label="About" severity="secondary" text/>
                    </RouterLink>
                    <RouterLink :to="{name:'features'}">
                        <Button label="Pricing" severity="secondary" text/>
                    </RouterLink>
                    <RouterLink :to="{name:'features'}">
                        <Button label="Contact" severity="secondary" text/>
                    </RouterLink>
                    <router-link :to="{name:'login'}">
                        <Button label="Login" severity="contrast" outlined/>
                    </router-link >
                    <router-link :to="{name:'register'}">
                        <Button label="Registro" severity="contrast" raised/>
                    </router-link>
                </div>   
            </div>
        </transition>
        <div class="flex justify-center">
            <!-- <RouterView /> -->
            <Landing/>
        </div>
        
    </div>
</template>
<script setup>
    import { ref } from 'vue';
    import Landing from "/src/views/Landing.vue"
    import IconMenu from "/src/components/icons/IconMenu.vue"
    import IconClose from "/src/components/icons/IconClose.vue"
    


    defineOptions({
        name: 'Guests',       
    });
const showMenu = ref(false);
const AppearMenu = ref(false);
    
    const showMobileMenu = () => {
        showMenu.value = !showMenu.value
    }


    setTimeout(() => {
        AppearMenu.value=true
    }, 500);

</script>