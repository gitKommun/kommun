<template>
  <section class="relative w-full  overflow-hidden px-6">
    <div class="w-full flex justify-center mb-12">
     <DotAnimation class="w-56"/>
    </div>
    <div class="w-full text-center text-2xl font-bold">
      Impulsando la gestión de las mejores comunidades.
    </div>
    <div class="w-full text-center text-xl text-slate-500 mt-2">
      Desde pequeñas comunidades hasta grandes urbanizaciones consolidadas.
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
