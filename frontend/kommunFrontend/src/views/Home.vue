<template>
    
        <div class="h-full w-full  pt-16 px-24">

            <section class="container mx-auto flex flex-col md:flex-row items-center justify-between py-12 px-6">
  <div class="md:w-1/2 mb-8 md:mb-0">
    <h1 class="text-6xl font-bold text-gray-800 mb-4">Tu aplicación de autogestión para comunidades</h1>
    <p class="text-lg text-gray-600 mb-8">Kommun es la solución definitiva para tu comunidad de vecinos. Gestiona pagos, organiza reuniones, votaciones y mucho más, todo en un solo lugar.</p>
    <vs-button color="dark"  size="xl">Registrar mi comunidad</vs-button>
  </div>
  <div class="md:w-1/2">
    <img src="@/assets/comu_1.png" alt="Imagen de la comunidad" class="w-full h-auto md:rounded-lg">
  </div>
</section>
        </div>
    
</template>
<script setup >
    import Guests from '/src/layouts/Guests.vue';
    defineOptions ({
        name: 'Home',
        layout: Guests,
    });
</script>