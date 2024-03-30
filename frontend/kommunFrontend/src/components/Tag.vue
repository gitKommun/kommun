<template>
  <div
    class="hr-tag flex h-6 max-w-min min-w-0 items-center whitespace-nowrap rounded-lg px-2 text-xs"
    :class="wrapperClass"
    v-on="$attrs"
  >
    <span class="leading-none truncate">
      <slot />
    </span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
defineOptions({
        name: 'tag',
        
    });

const TAG_COLORS = [
    'info',
    'success',
    'warning',
    'danger',
    'aqua',
    'candy',
    'golden',
    'grass',
    'pink',
    'purple',
    'steel',
    'sunrise',
    'turquoise',
    'amber',
    'lime',
    'blue',
    'violet',
];
const TAG_TYPES = ['default', 'solid'];

const color = ref('info');
const type = ref('default');

const wrapperClass = computed(() => {
    return [ `tag-${color.value}-${type.value}` ];
});

</script>

<style scoped>

.tag-info-default {
  @apply bg-slate-200 text-slate-700;
}
.tag-info-solid {
  @apply bg-slate-950 text-white;
}
.tag-success-default {
  @apply bg-green-200 text-green-700;
}
.tag-success-solid {
  @apply bg-green-500 text-white;
}
.tag-warning-default {
  @apply bg-yellow-200 text-yellow-700;
}
.tag-warning-solid {
  @apply bg-yellow-500 text-white;
}
.tag-danger-default {
  @apply bg-red-200 text-red-700;
}
.tag-danger-solid {
  @apply bg-red-500 text-white;
}
.tag-aqua-default {
  @apply bg-cyan-200 text-cyan-700;
}
.tag-aqua-solid {
  @apply bg-cyan-500 text-white;
}
.tag-candy-default {
  @apply bg-fuchsia-200 text-fuchsia-700;
}
.tag-candy-solid {
  @apply bg-fuchsia-500 text-white;
}
.tag-pink-default {
  @apply bg-pink-200 text-pink-700;
}
.tag-pink-solid {
  @apply bg-pink-500 text-white;
}
.tag-purple-default {
  @apply bg-purple-200 text-purple-700;
}
.tag-purple-solid {
  @apply bg-purple-500 text-white;
}
.tag-sunrise-default {
  @apply bg-orange-200 text-orange-700;
}
.tag-sunrise-solid {
  @apply bg-orange-500 text-white;
}
.tag-turquoise-default {
  @apply bg-teal-200 text-teal-700;
}
.tag-turquoise-solid {
  @apply bg-teal-500 text-white;
}
.tag-lime-default {
  @apply bg-lime-200 text-lime-700;
}
.tag-lime-solid {
  @apply bg-lime-500 text-white;
}
.tag-blue-default {
  @apply bg-blue-200 text-blue-700;
}
.tag-blue-solid {
  @apply bg-blue-500 text-white;
}
.tag-amber-default {
  @apply bg-amber-200 text-amber-700;
}
.tag-amber-solid {
  @apply bg-amber-500 text-white;
}
.tag-violet-default {
  @apply bg-violet-200 text-violet-700;
}
.tag-violet-solid {
  @apply bg-violet-500 text-white;
}
</style>