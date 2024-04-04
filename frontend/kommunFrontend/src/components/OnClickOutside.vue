<script setup>
import { onMounted, onUnmounted } from 'vue';

const listener = (event) => {
  if (props.disabled || event.target === $el || $el.contains(event.target)) {
    return;
  }
  props.do();
};

onMounted(() => {
  document.addEventListener('click', listener);
});

onUnmounted(() => {
  document.removeEventListener('click', listener);
});
</script>

<template>
  <slot></slot>
</template>
