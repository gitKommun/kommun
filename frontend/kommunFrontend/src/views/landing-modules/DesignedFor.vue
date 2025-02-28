<template>
  <section
    class="container max-w-[1280px] mx-auto flex flex-col items-start py-12 mt-20 px-6"
  >
    <h1 class="text-4xl md:text-5xl font-bold text-slate-900 mb-6 text-center md:text-left">
      <span
        class="text-transparent bg-clip-text bg-gradient-to-r from-violet-500 to-teal-400"
        >Diseñado para la gestión</span
      >
      <br />moderna de comunidades
    </h1>
    <p  class="text-lg text-slate-600 mb-16  text-center md:text-left ">
      Nuestro SaaS se basa en prácticas y principios que distinguen a las
      comunidades mejor gestionadas: <br />
      enfoque constante, gestión eficiente y un firme compromiso con la calidad
      en cada detalle.
    </p>

    <div class="w-full flex flex-col md:flex-row justify-center pb-16 gap-6 ">
      <div class="w-full bg-slate-50 border border-200 rounded-2xl overflow-hidden">
        <div class="h-72 flex items-center justify-center">
          <ManagementCommunities class="scale-50"/>
        </div>
        <div class=" font-bold text-slate-900 text-center p-4">Creado específicamente para la gestión de comunidades.</div>
      </div>
      <div class="w-full bg-slate-50 border border-200 rounded-2xl overflow-hidden">
        <div class="h-72  flex items-center justify-center">
          <AgilityProcess class="scale-50"/>
        </div>
        <div class="font-bold text-slate-900 text-center p-4">Diseñado para agilizar procesos.</div>
      </div>
      <div class="w-full bg-slate-50 border border-200 rounded-2xl overflow-hidden">
        <div class="h-72  flex items-center justify-center">
          <ExperienceDesign class="scale-50"/>
        </div>
        <div class=" font-bold text-slate-900 text-center p-4">Perfeccionado para ofrecer la mejor experiencia.</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import AgilityProcess from './AgilityProcess.vue';
import ExperienceDesign from './ExperienceDesign.vue';
import ManagementCommunities from './ManagementCommunities.vue';
</script>
