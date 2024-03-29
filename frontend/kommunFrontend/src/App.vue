<template>
  <div class="h-screen w-screen">

    <RouterView v-slot="{ Component }">
      <Component :is="layout">
        <Component :is="Component" />
      </Component>
    </RouterView>
  </div>
  
</template>
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useLayout } from '/src/composables/useLayout';

// layout
    const layout = useLayout('div');
</script>


