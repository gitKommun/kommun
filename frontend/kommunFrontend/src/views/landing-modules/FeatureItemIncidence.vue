<template>
    <section class="flex flex-col items-center py-3 w-full duration-500" v-animateonscroll="{ enterClass: 'animate-zoomin', leaveClass: 'animate-fadeout' }">
        <div class=" max-w-[1280px] flex  justify-center items-center py-6 mb-8 flex-col md:flex-row">

            <div class="flex justify-center items-center backdrop-blur-xl bg-gradient-to-tr from-white/5  to-white/15 rounded-3xl shadow-2xl p-4 perspective-item "
               >
                            <img class="h-40 -rotate-45" src="@/assets/incidences2.svg">
            </div>
            <div class="flex flex-col py-2 text-white ml-12 max-w-screen-sm"
                >
                <span class="font-bold text-3xl mb-3 text-transparent bg-clip-text bg-gradient-to-r from-amber-600  to-yellow-300">Gestión de Incidencias</span>
                <span class="text-slate-400 "> Resuelve cualquier incidencia de manera rápida y eficiente, con total transparencia. Kommun te permite mantener todo bajo control y a los vecinos siempre informados.</span>
            </div>
        </div>
       
    </section>   
</template>

<script setup >
    import { ref, shallowRef } from 'vue'
    import IconTool from "/src/components/icons/IconTool.vue"


    defineOptions ({
        name: 'FeaturesItemIncidence'
    });
  

</script>
<style>
.perspective-item {
  transform: rotateX(51deg) rotateZ(30deg);
  transform-style: preserve-3d;
  border-radius: 32px;
  box-shadow:
    1px 1px 0 1px rgba(255, 255, 255, 0.25),
    -1px 0 28px 0 rgba(0, 0, 0, 0.04),
    28px 28px 28px 0 rgba(0, 0, 0, 0.35);
  transition: 0.4s ease-in-out transform,
              0.4s ease-in-out box-shadow;
}

.perspective-item:hover {
  transform: translate3d(0px, -16px, 0px) rotateX(51deg) rotateZ(50deg);
  box-shadow:
    1px 1px 0 1px rgba(255, 255, 255, 0.25),
    -1px 0 28px 0 rgba(0,0,0, 0.04),
    54px 54px 28px -10px rgba(0,0,0, 0.35);
}
</style>