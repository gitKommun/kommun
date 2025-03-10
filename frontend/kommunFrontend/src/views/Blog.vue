<template>
  <div class="container mx-auto pt-24 px-4 md:px-6">
    <!-- Primera sección: Post destacado + 4 posts recientes -->
    <section class="mb-12">
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- Columna principal (60%) -->
        <div class="w-full lg:w-[60%]">
          <article class="bg-white rounded-lg shadow-md overflow-hidden h-full">
            <div class="relative aspect-[16/9]">
              <img 
                src="https://picsum.photos/800/450"
                alt="Post principal" 
                class="w-full h-full object-cover"
              />
            </div>
            <div class="p-6">
              <div class="text-sm text-gray-500 mb-2">
                12 Marzo, 2024
              </div>
              <h2 class="text-2xl font-bold mb-3 text-gray-800">
                Título del post principal
              </h2>
              <p class="text-gray-600 line-clamp-3 mb-4">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
              </p>
              <button class="text-purple-600 font-semibold hover:text-purple-800 transition-colors">
                Saber más →
              </button>
            </div>
          </article>
        </div>

        <!-- Columna secundaria (40%) - Posts más compactos -->
        <div class="w-full lg:w-[40%]">
          <div class="grid gap-4"> <!-- Reducido el gap -->
            <!-- 4 posts secundarios -->
            <article v-for="i in 4" :key="i" class="bg-white rounded-lg shadow-sm overflow-hidden flex flex-row">
              <div class="relative w-1/3 aspect-[4/3]"> <!-- Cambiado aspect ratio -->
                <img 
                  :src="`https://picsum.photos/600/338?random=${i}`"
                  :alt="`Post secundario ${i}`" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-3 flex-1"> <!-- Reducido el padding -->
                <div class="text-xs text-gray-500 mb-1">
                  12 Marzo, 2024
                </div>
                <h3 class="font-bold text-base mb-1 text-gray-800"> <!-- Reducido el tamaño del título -->
                  Título del post secundario
                </h3>
                <p class="text-gray-600 text-xs line-clamp-2 mb-2">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                </p>
                <button class="text-purple-600 text-xs font-semibold hover:text-purple-800 transition-colors">
                  Saber más →
                </button>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>

    <!-- Segunda sección: Lista de posts en formato horizontal -->
    <section>
      <h2 class="text-2xl font-bold mb-6 text-gray-800">Más artículos</h2>
      <div class="grid gap-6">
        <article v-for="i in 6" :key="i" class="bg-white rounded-lg shadow-md overflow-hidden flex flex-col sm:flex-row">
          <div class="relative sm:w-1/3 aspect-[16/9] sm:aspect-[16/10]">
            <img 
              :src="`https://picsum.photos/400/225?random=${i + 10}`"
              :alt="`Post listado ${i}`" 
              class="w-full h-full object-cover"
            />
          </div>
          <div class="flex-1 p-6">
            <div class="text-sm text-gray-500 mb-2">
              12 Marzo, 2024
            </div>
            <h3 class="font-bold text-xl mb-3 text-gray-800">
              Título del post en lista
            </h3>
            <p class="text-gray-600 line-clamp-3 mb-4">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            </p>
            <button class="text-purple-600 font-semibold hover:text-purple-800 transition-colors">
              Saber más →
            </button>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import Guests from '/src/layouts/Guests.vue';

defineOptions({
  name: 'Blog',
  layout: Guests,
});
</script>


