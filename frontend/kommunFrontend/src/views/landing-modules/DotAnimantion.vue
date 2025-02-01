<template>
  <div class=" flex items-center relative">
    <div class="flex items-center justify-center size-10 md:size-16 bg-slate-50 border border-slate-200 mx-1 transition-all duration-300 rounded-xl md:rounded-2xl" :class="{'translate-x-12 opacity-0':step===2 || step===1}">
      <SmallHome v-if="step===0" class="h-4 md:h-6"/>
    </div>
    <div class="flex items-center justify-center size-12 md:size-24 bg-slate-50 border border-slate-200 mx-1 transition-all duration-300 rounded-xl md:rounded-2xl" :class="{'translate-x-16 opacity-0':step===2 }">
      <SmallHome v-if="step===0" class="h-6 md:h-10"/>
      <MediumHome v-if="step===1" class="h-6 md:h-10"/>
    </div>
    <div class="flex items-center justify-center size-16 md:size-32 bg-slate-50 border border-slate-200 mx-1 transition-all duration-300 rounded-xl md:rounded-2xl">
      <SmallHome v-if="step===0" class="h-8 md:h-12"/>
      <MediumHome v-if="step===1" class="h-8 md:h-12"/>
      <LargeHome v-if="step===2" class="h-8 md:h-12"/>
    </div>
    <div class="flex items-center justify-center size-16 md:size-32 bg-slate-50 border border-slate-200 mx-1 transition-all duration-300 rounded-xl md:rounded-2xl">
      <SmallHome v-if="step===0" class="h-8 md:h-12"/>
      <MediumHome v-if="step===1" class="h-8 md:h-12"/>
      <LargeHome v-if="step===2" class="h-8 md:h-12"/>
    </div>
    <div class="flex items-center justify-center size-12 md:size-24 bg-slate-50 border border-slate-200 mx-1 transition-all duration-300 rounded-xl md:rounded-2xl" :class="{'-translate-x-16 opacity-0':step===2 }">
      <SmallHome v-if="step===0" class="h-6 md:h-10"/>
      <MediumHome v-if="step===1" class="h-6 md:h-10"/>
    </div>
    <div class="flex items-center justify-center size-10 md:size-16 bg-slate-50 border border-slate-200 mx-1 transition-all duration-300 rounded-xl md:rounded-2xl" :class="{'-translate-x-12 opacity-0':step===2 || step===1}">
      <SmallHome v-if="step===0" class="h-4 md:h-6"/>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import SmallHome from '@/components/svgs/SmallHome.vue';
import MediumHome from '@/components/svgs/MediumHome.vue';
import LargeHome from '@/components/svgs/LargeHome.vue';
const step = ref(0);
setInterval(() => {
  step.value = (step.value + 1) % 3;
}, 3000);

</script>
