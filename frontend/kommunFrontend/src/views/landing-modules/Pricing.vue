<template>
    <section class="flex flex-col items-center py-12">
        <div class=" max-w-[1280px] flex flex-col justify-center items-center py-6 mb-8">
            <h2 class="text-2xl mb-3 text-slate-950 font-bold">Lorem ipsum dolor sit amet, consectetur adipiscing elit</h2>
            <p class="text-slate-950">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        </div>
        <div class="">
            <div class="flex justify-center max-w-[24rem] m-auto mb-8 lg:mb-16">
                <div class="relative flex w-full p-2 bg-slate-900 rounded-full">
                    <span class="absolute inset-0 m-1 pointer-events-none" aria-hidden="true">
                        <span class="absolute inset-0 w-1/2 bg-cyan-500 rounded-full shadow-sm shadow-cyan-950/10 transform transition-transform duration-150 ease-in-out" :class="isAnnual ? 'translate-x-0' : 'translate-x-full'"></span>
                    </span>
                    <button
                        class="relative flex-1 px-4 font-medium h-12 rounded-lg focus-visible:outline-none focus-visible:ring focus-visible:ring-cyan-300  transition-colors duration-150 ease-in-out"
                        :class="isAnnual ? 'text-white' : 'text-slate-500 dark:text-slate-400'"
                        @click="isAnnual = true"
                        :aria-pressed="isAnnual"
                    >
                        Yearly 
                        <span :class="isAnnual ? 'text-cyan-200' : 'text-slate-400'">-20%</span>
                    </button>
                    <button
                        class="relative flex-1  px-4 font-medium h-12 rounded-lg focus-visible:outline-none focus-visible:ring focus-visible:ring-cyan-300  transition-colors duration-150 ease-in-out"
                        :class="isAnnual ? 'text-slate-500' : 'text-white'"
                        @click="isAnnual = false"
                        :aria-pressed="isAnnual"
                    >
                        Monthly
                    </button>
            </div>
        </div>
        </div>
        <div class="max-w-[1280px] container mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-4">
            <div class="bg-white rounded-2xl border border-slate-200 p-4 gap-x-3 flex hover:shadow-xl transition-all durations-300">
                <div class="p-3 w-full">
                    <h3 class="text-4xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-pink-600 to-yellow-400">Free</h3>
                    <p class="text-slate-500 text-sm text-center">Ideal para pequeñas comunidades</p>
                    <h1 class="text-6xl font-bold text-center py-4">0€ <span class="text-sm text-slate-500 font-regular">/mes</span></h1>
                    <vs-button color="dark" block size="large">Let start</vs-button>
                    <div class="border-t border-slate-200 mt-3 py-3">
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Foro para miembros</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Votaciones</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Documentación</div>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-2xl border border-slate-200 p-4 gap-x-3 flex hover:shadow-xl transition-all durations-300">
                <div class="p-3 w-full">
                    <h3 class="text-4xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-cyan-400">Basic</h3>
                    <p class="text-slate-500 text-sm text-center">Ideal para pequeñas comunidades</p>
                    <h1 class="text-6xl font-bold text-center py-4">15€ <span class="text-sm text-slate-500 font-regular">/mes</span></h1>
                    <vs-button color="dark" block size="large">Let start</vs-button>
                    <div class="border-t border-slate-200 mt-3 py-3">
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Foro para miembros</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Votaciones</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Documentación</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Incidencias</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Presupuestos</div>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-2xl border border-slate-200 p-4 gap-x-3 flex hover:shadow-xl transition-all durations-300">
                <div class="p-3 w-full">
                    <h3 class="text-4xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-pink-400">Advanced</h3>
                    <p class="text-slate-500 text-sm text-center">Todo lo que tu comunidad necesita</p>
                    <h1 class="text-6xl font-bold text-center py-4">25€ <span class="text-sm text-slate-500 font-regular">/mes</span></h1>
                    <vs-button color="dark" block size="large">Let start</vs-button>
                    <div class="border-t border-slate-200 mt-3 py-3">
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Foro para miembros</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Votaciones</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Documentación</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Incidencias</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Presupuestos</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Reserva de espacios</div>
                        <div class="flex py-2 text-sm text-slate-500"> <IconCircleCheck class="scale-75 text-green-500 mr-3"/> Proveedores</div>
                    </div>
                </div>
            </div>   
        </div>
    </section> 
</template>
<script setup>
import { ref } from 'vue';
import IconCircleCheck from "/src/components/icons/IconCircleCheck.vue"


defineOptions({
    name:'Pricinng'
})

const isAnnual = ref(true); // Estado inicial: anual
</script>