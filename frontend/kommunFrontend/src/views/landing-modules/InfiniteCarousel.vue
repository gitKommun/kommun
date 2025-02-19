<template>
  <div class="relative w-[350px] mx-auto overflow-visible h-[200px]">
    <div 
      class="flex gap-4 transition-transform duration-500 ease-in-out"
      :style="{ transform: `translateX(${position}px)` }"
    >
      <div 
        v-for="(item, index) in displayItems" 
        :key="index"
        class="min-w-[60px] min-h-[60px] rounded-2xl bg-slate-50 border border-slate-200 transition-all duration-300 ease-in-out flex items-center justify-center text-2xl relative"
        :class="{
          'scale-100': index === currentIndex + 2,
          'scale-[0.857]': index === currentIndex + 1 || index === currentIndex + 3,
          'scale-[0.619]': index === currentIndex || index === currentIndex + 4,
          'opacity-0': index < currentIndex || index > currentIndex + 4
        }"
      >
        <div class="w-full h-full flex items-center justify-center">
          <component
                :is="ICONS[item.type]"
                :class="`${item.color}`"
            />
        </div>
        <div 
          class="absolute -bottom-24 left-1/2 -translate-x-1/2 w-[200px] h-24  flex flex-col items-center justify-center text-white transition-all duration-500 ease-in-out z-10"
          :class="{
            'opacity-100 translate-y-0': index === currentIndex + 2,
            'opacity-0 translate-y-8': index !== currentIndex + 2
          }"
        >
        <div class="w-[2px] h-24 bg-slate-200"></div>
        <span class="uppercase text-slate-500 text-sm mt-2">{{ item.text }}</span>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import IconFlag from '@/components/icons/IconFlag.vue';
import IconPin from '@/components/icons/IconPin.vue';
import IconStar from '@/components/icons/IconStar.vue';
import IconMessage from '@/components/icons/IconMessage.vue';
import IconAutomation from '@/components/icons/IconAutomation.vue';
import IconWorker from '@/components/icons/IconWorker.vue';
import IconTag from '@/components/icons/IconTag.vue';
import IconBell from '@/components/icons/IconBell.vue';


//const items = ref([1, 2, 3, 4, 5, 6]);
const currentIndex = ref(0);
const items = ref([
    {
        type: 'priority',
        text: 'Priorización ',
        color: 'text-red-500',
    },
    {
        type: 'location',
        text: 'Ubicación',
        color: 'text-blue-500',
    },
    {
        type: 'rating',
        text: 'Valoración',
        color: 'text-amber-500',
    },
    {
        type: 'comments',
        text: 'Comunicación',
        color: 'text-teal-500',
    },
    {
        type: 'automation',
        text: 'Automatización',
        color: 'text-purple-500',
    },
    {
        type: 'providers',
        text: 'Proveedores',
        color: 'text-orange-500',
    },
    {
        type: 'status',
        text: 'Estado',
        color: 'text-green-500',
    },
    {
        type: 'notifications',
        text: 'Notificaciones',
        color: 'text-indigo-500',
    }
])

const ICONS = {
    priority: IconFlag,
    location: IconPin,
    rating: IconStar,
    comments: IconMessage,
    automation: IconAutomation,
    providers: IconWorker,
    status: IconTag,
    notifications: IconBell,
}

// Calculamos la posición inicial para centrar perfectamente
const initialPosition = computed(() => {
  const containerWidth = 350;
  const itemWidth = 60;
  const itemGap = 16; // equivalente a gap-4
  return (containerWidth - itemWidth) / 2 - (itemWidth + itemGap) * 2;
});

const position = ref(initialPosition.value);

const displayItems = computed(() => {
  return [...items.value, ...items.value, ...items.value,...items.value, ...items.value, ...items.value,...items.value, ...items.value, ...items.value];
});

const moveCarousel = () => {
  position.value -= (60 + 16); // ancho del item + gap
  currentIndex.value++;
  
  if (currentIndex.value >= items.value.length) {
    setTimeout(() => {
      position.value = initialPosition.value;
      currentIndex.value = 0;
    }, 0);
  }
};

onMounted(() => {
  setInterval(moveCarousel, 3000);
});
</script>

