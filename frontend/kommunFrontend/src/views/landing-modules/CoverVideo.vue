<template>
    <section class="relative w-full h-screen overflow-hidden">

        <img src="@/assets/bg.jpg"  class="absolute top-0 left-0 w-full h-full object-cover">

        <!-- Contenido superpuesto -->
         <transition
            enter-from-class="mt-24 opacity-0"
            enter-active-class="transitiona-all ease-in-out duration-500"
            move-class="transitiona-all bounce-transition duration-300"
            >
            <div v-if="AppearInfo" class="relative z-10 flex  justify-center items-center h-full flex-col md:flex-row md:px-8 lg:px-16 ">
                <div class="md:w-1/2 mb-8 md:mb-0 text-center md:text-left pl-8 pr-8 md:pl-12">
                    <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">Donde la Transparencia y la Eficiencia se Encuentran</h1>
                    <p class="text-lg text-white mb-8">En Kommun, simplificamos la gestión de tu comunidad, asegurando transparencia y participación en cada decisión, sin complicaciones ni sorpresas.</p>
                    <router-link :to="{name:'register'}">
                        <Button 
                            severity="contrast" 
                            label="Registrar mi comunidad" 
                            raised   
                            size="large"/>
                    </router-link>
                    
                </div>
                <div class="md:w-1/2 flex justify-center items-center px-12 md:px-0">
                    <div class="flex justify-center items-center backdrop-blur-xl bg-gradient-to-tr from-white/15  to-white/50 rounded-3xl shadow-2xl p-4 perspective transition-all">
                            <img src="@/assets/house.svg">
                    </div>
                    
                </div>

                
            </div>
        </transition>
    </section>
</template>
<script setup>
    import { ref } from 'vue';
    
    defineOptions({
        name: 'CoverV',       
    });

    const AppearInfo = ref(false);
    
    setTimeout(() => {
        AppearInfo.value=true
    }, 1000);

</script>
<style>
.perspective {
  transform: rotateX(51deg) rotateZ(43deg);
  transform-style: preserve-3d;
  border-radius: 32px;
  box-shadow:
    1px 1px 0 1px rgba(255, 255, 255, 0.75),
    -1px 0 28px 0 rgba(34, 33, 81, 0.04),
    28px 28px 28px 0 rgba(34, 33, 81, 0.35);
  transition: 0.4s ease-in-out transform,
              0.4s ease-in-out box-shadow;
}

.perspective:hover {
  transform: translate3d(0px, -16px, 0px) rotateX(51deg) rotateZ(43deg);
  box-shadow:
    1px 1px 0 1px rgba(255, 255, 255, 0.75),
    -1px 0 28px 0 rgba(34, 33, 81, 0.04),
    54px 54px 28px -10px rgba(34, 33, 81, 0.35);
}
</style>