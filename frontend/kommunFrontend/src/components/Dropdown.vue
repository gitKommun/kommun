<template>
    
</template>
<!-- <template>
    <OnClickOutside :do="close">
    <div class="relative inline-block">
        <div
        ref="reference"
        @click="toggle"
        class="relative"
        :class="referenceClass"
        >
        <slot name="reference" :isOpen="isOpen" />
        </div>
        <div
        ref="content"
        v-if="isOpen"
        class="bg-red-500 rounded-2xl p-3"
        :class="contentClass"
        >
        <slot name="content" :isOpen="isOpen" :close="close" />
        </div>
    </div>
  </OnClickOutside>
</template>

<script setup>
import { ref, watch, onUnmounted, nextTick, defineProps, emit } from 'vue';
import { createPopper } from '@popperjs/core';
import OnClickOutside from '/src/components/OnClickOutside.vue'

const reference = ref(null);
const content = ref(null);
const dropdown = ref(null);
const isOpen = ref(false);

const props = defineProps({
    placement: {
      type: String,
      default: 'bottom',
    },
    offset: {
      type: Array,
      default: () => [0, 8],
    },
    modifiers: {
      type: Array,
      default: () => [],
    },
    strategy: {
      type: String,
      default: 'absolute',
    },
    referenceClass: {
      type: String,
      default: '',
    },
    contentClass: {
      type: String,
      default: '',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
})

const toggle = () => {
  if (!isOpen.value) {
    open();
  } else {
    close();
  }
};

const open = () => {
  if (!disabled.value) {
    isOpen.value = true;
    emit('change', true);
  }
};

const close = () => {
  if (!disabled.value) {
    isOpen.value = false;
    emit('change', false);
  }
};

const update = () => {
  if (dropdown.value) {
    dropdown.value.update();
  }
};

const setupDropdown = () => {
  dropdown.value = createPopper(reference.value, content.value, {
    placement: placement.value,
    strategy: strategy.value,
    modifiers: [
      {
        name: 'offset',
        options: {
          offset: offset.value,
        },
      },
      ...modifiers.value,
    ],
  });
};

const destroyDropdown = () => {
  if (dropdown.value) {
    dropdown.value.destroy();
  }
};

watch(isOpen, async (open) => {
  if (open) {
    await nextTick();
    setupDropdown();
  } else {
    destroyDropdown();
  }
});

onUnmounted(() => {
  destroyDropdown();
});
</script>



 -->
