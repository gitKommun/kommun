<template>
  <span :class="computedClasses" class="flex items-center">
    <slot></slot>
  </span>
</template>

<script setup>
import { computed } from 'vue';

defineOptions({
    name: 'customTag',
})

const props = defineProps({
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['gray', 'red', 'yellow', 'green', 'blue', 'indigo', 'purple', 'pink', 'orange','amber','lime','emerald','teal','cyan','sky','violet','fuchsia','rose'].includes(value),
  },
  solid: {
    type: Boolean,
    default: false
  }
  
});
const computedClasses = computed(() => {
  if (props.solid) {
    return `h-6 px-2 py-1 rounded-md text-xs text-${props.color}-100 bg-${props.color}-500`;
  }
  return `h-6 px-2 py-1 rounded-md text-xs text-${props.color}-600 bg-${props.color}-100`;
});
</script>
