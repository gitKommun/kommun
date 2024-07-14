<template>
  <div class="h-screen w-screen text-slate-950">
    <RouterView v-slot="{ Component }">
      <transition
        enter-active-class="transition-all transition-slow ease-out overflow-hidden"
        leave-active-class="transition-all transition-slow ease-in overflow-hidden"
        enter-class="opacity-0"
        enter-to-class="opacity-100"
        leave-class="opacity-100"
        leave-to-class="opacity-0"
        mode="out-in"
      >
        <Component :is="layout">
          <Component :is="Component" />
        </Component>
      </transition>
    </RouterView>
    
  </div>
  
</template>
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useLayout } from '/src/composables/useLayout';

// layout
    const layout = useLayout('div');
</script>


