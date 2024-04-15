<template>
  <span :class="computedClasses">
    <slot></slot>
  </span>
</template>

<script setup>
import { computed } from 'vue';



const props = defineProps({
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['gray', 'red', 'yellow', 'green', 'blue', 'indigo', 'purple', 'pink', 'orange','amber','lime','emerald','teal','cyan','sky','violet','fuchsia','rose'].includes(value),
  },
  
});
const computedClasses = computed(() => {
  return `h-6 px-2 py-1 rounded-md text-xs text-${props.color}-100 bg-${props.color}-500`;
});
</script>
