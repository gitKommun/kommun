<template>
  <div class="flex justify-center px-3 pb-6">
    <div class="w-full max-w-4xl flex flex-col gap-y-3">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineOptions({
  name: "Content",
});
</script>
