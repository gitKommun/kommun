<template>
  <section
    class="container max-w-[1280px] mx-auto flex flex-col md:flex-row items-start py-12 my-20 px-6"
  >
    <div class="w-full md:w-1/2 overflow-hidden order-2 md:order-1">
      <InfiniteCarousel />
    </div>
    <div class="w-full md:w-1/2 order-1 md:order-2">
      <h1
        class="text-4xl md:text-5xl font-bold text-gray-800 mb-4 text-center md:text-left"
      >
        <span
          class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-orange-400"
          >Gestión de incidencias</span
        >
        <br />Simple y eficiente
      </h1>
      <p class="text-lg text-gray-600 mb-8 text-center md:text-left">
        Aborda problemas en su contexto y gestiona todo con herramientas
        diseñadas para agilizar la comunicación y colaboración en tu comunidad.
      </p>
    </div>
  </section>
</template>

<script setup>
import InfiniteCarousel from "./InfiniteCarousel.vue";
</script>
