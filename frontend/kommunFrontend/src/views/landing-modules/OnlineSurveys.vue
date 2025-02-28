<template>
  <section
    class="container max-w-[1280px] mx-auto flex flex-col md:flex-row items-start py-12 my-20 px-6 gap-6"
  >
  <div class="w-full md:w-1/2 ">
      <h1
        class="text-4xl md:text-5xl font-bold text-slate-900 mb-6 text-center md:text-left"
      >
        <span
          class="text-transparent bg-clip-text bg-gradient-to-r from-violet-500 to-pink-400"
          >Votaciones online</span
        >
        <br />rápidas y seguras
      </h1>
      <p class="text-lg text-slate-600 mb-8 text-center md:text-left">
        Facilita la toma de decisiones en tu comunidad con un sistema de votación digital. 
        Seguro, accesible y en tiempo real, para que todos los vecinos participen sin complicaciones.
      </p>
      <Button severity="contrast"  raised size="large"> Solicitar una demo <IconChevronRight/> </Button>
    </div>
    <div class="w-full h-full md:w-1/2">
       <div class="w-full h-full border border-slate-200 bg-slate-50 rounded-2xl flex items-center justify-center">
        <OnlineSurveysImage class="scale-50"/>
       </div>
    </div>
    
  </section>
</template>

<script setup>
import OnlineSurveysImage from "./OnlineSurveysImage.vue";
import IconChevronRight from '@/components/icons/IconChevronRight.vue';
</script>
