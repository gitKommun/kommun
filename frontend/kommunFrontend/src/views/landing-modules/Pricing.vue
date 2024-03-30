<template>
    <section class="flex flex-col items-center py-12">
        <div class=" max-w-[1280px] flex flex-col justify-center items-center py-6 mb-8">
            <h2 class="text-2xl mb-3 text-slate-950 font-bold">Lorem ipsum dolor sit amet, consectetur adipiscing elit</h2>
            <p class="text-slate-950">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        </div>
        <div class="">
            <vs-switch v-model="AnnualPlan" color="success">
                <template #off> Monthly </template>
                <template #on> Annual </template>
            </vs-switch>
            <span>ahorra 2 meses</span>
        </div>
        <div class="max-w-[1280px] container mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div 
                class="bg-white rounded-2xl shadow-md p-4 gap-x-3 flex hover:shadow-xl transition-all durations-300"
                >
                
                <div class="p-3 w-full">
                    <h3 class="text-4xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-violet-500 to-cyan-500">Básico</h3>
                    <p class="text-slate-500 text-sm text-center">Ideal para pequeñas comunidades</p>
                </div>
            </div>    
        </div>
    </section> 
</template>
<script setup>
import { ref } from 'vue';

defineOptions({
    name:'Pricinng'
})

const AnnualPlan = ref(true);
</script>