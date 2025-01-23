<template>
  <section class="relative w-full h-screen overflow-hidden px-6">
    <div class="w-full text-center text-2xl font-bold">
      Impulsando la gestión de las mejores comunidades.
    </div>
    <div class="w-full text-center text-xl text-slate-500 mt-2">
      Desde pequeñas comunidades hasta grandes urbanizaciones consolidadas.
    </div>
    <div class="w-full flex justify-center mt-12">
     <DotAnimation/>
    </div>
  </section>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import DotAnimation from "/src/views/landing-modules/DotAnimantion.vue";

defineOptions({
  name: "multiCommunity",
});

</script>
<style></style>
