<template>

    <div
      class="bg-slate-50 flex flex-wrap"
      :style="containerStyle"
    >
      <transition-group name="slide" tag="div" class="flex flex-wrap">
        <div
          v-for="(point, index) in visiblePoints"
          :key="index"
          class="w-4 h-4 rounded-full m-1"
          :style="{ backgroundColor: point.color }"
        ></div>
      </transition-group>
    </div>

</template>

<script setup>
import { ref, computed, watchEffect } from 'vue';

const pointsConfig = [
  { count: 12, color: 'blue' },
  { count: 44, color: 'pink' },
  { count: 120, color: 'amber' },
];

const points = ref([]);
const visiblePoints = ref([]);
const currentSetIndex = ref(0);
const containerStyle = computed(() => {
  const size = Math.ceil(Math.sqrt(points.value.length));
  return {
    display: 'grid',
    gridTemplateColumns: `repeat(${size}, 1fr)`,
    maxWidth: '300px',
    gap: '5px',
    transition: 'width 0.5s ease-in-out',
  };
});

const startAnimation = () => {
  if (currentSetIndex.value >= pointsConfig.length) {
    currentSetIndex.value = 0;
  }

  const { count, color } = pointsConfig[currentSetIndex.value];
  points.value = Array.from({ length: count }, () => ({ color }));
  visiblePoints.value = [];

  let i = 0;
  const interval = setInterval(() => {
    if (i >= points.value.length) {
      clearInterval(interval);
      setTimeout(() => {
        currentSetIndex.value++;
        startAnimation();
      }, 1000);
    } else {
      visiblePoints.value.push(points.value[i]);
      i++;
    }
  }, 100);
};

watchEffect(() => {
  startAnimation();
});
</script>

<style scoped>
.slide-enter-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.slide-enter-from {
  transform: translateY(10px);
  opacity: 0;
}
.slide-enter-to {
  transform: translateY(0);
  opacity: 1;
}
.slide-leave-from {
  transform: translateY(0);
  opacity: 1;
}
.slide-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>
