<template>
     <div class="flex h-screen w-screen items-center justify-center px-8 py-6">
      <div class="flex max-w-160 flex-col items-center justify-center md:flex-row md:justify-start">
        <div class="mt-4 text-center ">
          <p class="text-6xl mb-8 font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300 inline-block transform scale-200">
            404
          </p>
          <p class="text-gray-500 mb-3">La página a la que intentas acceder no existe</p>
          <Button severity="contrast" @click="router.push('/')">Volver al sitio</Button>
        </div>
      </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

</script>
