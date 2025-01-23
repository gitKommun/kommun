<template>
  <section
    class="container max-w-[1280px] mx-auto flex flex-col items-start py-12 mt-20 px-6"
  >
    <h1  class=" text-4xl md:text-6xl font-bold text-gray-800 mb-4">
      Donde la <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-500 to-pink-400">Transparencia</span> y <br/> <span class="text-transparent bg-clip-text bg-gradient-to-r from-violet-500  to-sky-400">Eficiencia</span> se Encuentran
    </h1>
    <p ref="textTitle" class="text-lg text-gray-600 mb-8 animated-text ">
      Simplificamos la gestión de tu comunidad.<br/>
        Sin complicaciones ni sorpresas.
    </p>
    <div class="flex items-center gap-x-4">
        <Button severity="contrast" label="Comenzar" raised size="large" />
        <span class="flex items-center animate-pulse gap-x-2">Solicitar una demo <IconChevronRight/></span>
    </div>
    <div class="w-full flex justify-center pb-16 relative">
        <div class="m-auto rounded-2xl border border-slate-200 bg-slate-50 min-w-200 md:w-full  aspect-4/3 perspective_1 "></div>
        <div class="absolute inset-0 bg-gradient-to-tl from-white via-white/25 to-white/0  min-w-200 md:w-full  aspect-4/3 blur_perspective pointer-events-none"></div>
    </div>
  </section>
</template>
<script setup>
import { ref, onMounted } from "vue";
import IconChevronRight from '@/components/icons/IconChevronRight.vue';


const textTitle = ref(null);
const lines = ref([]);

onMounted(() => {
  if (textTitle.value) {
    // Extraer texto original
    const originalText = textTitle.value.innerText;

    // Dividirlo en líneas
    lines.value = originalText.split("\n").map((line) => line.trim());

    // Reemplazar el contenido original con líneas animadas
    textTitle.value.innerHTML = lines.value
      .map(
        (line, index) => `
          <p 
            class="line" 
            style="animation-delay: ${index * 0.3}s"
          >
            ${line}
          </p>
        `
      )
      .join("");
  }
});



</script>
<style>
.perspective_1 {
  transform: rotateX(-40deg) rotateZ(-25deg) translateX(15%);
  transform-style: preserve-3d;
  border-radius: 32px;

  transition: 0.4s ease-in-out transform,
              0.4s ease-in-out box-shadow;
}
.blur_perspective {
  transform: rotateX(-40deg) rotateZ(-25deg) translateX(15%) scale(1.2);
  transform-style: preserve-3d;
  border-radius: 32px;

}
.perspective_1:hover {
  transform: rotateX(-40deg) rotateZ(-25deg) translateX(15%) translateY(-16px);
  
     box-shadow:
    -1px 1px 0 1px rgba(255, 255, 255, 0.75),
    -1px 0 28px 0 rgba(34, 33, 81, 0.02),
    -28px 28px 28px 0 rgba(34, 33, 81, 0.1);
}
.animated-text {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* Espacio entre líneas */
}

.line {
  opacity: 0;
  filter: blur(10px);
  transform: translateY(10px);
  animation: fadeInBlur 1s ease-out forwards;
}

/* Animación */
@keyframes fadeInBlur {
  0% {
    opacity: 0;
    filter: blur(10px);
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    filter: blur(0);
    transform: translateY(0);
  }
}
</style>