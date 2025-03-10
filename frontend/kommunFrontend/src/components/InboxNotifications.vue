<template>
  <Dropdown strategy="fixed">
    <template #reference="{ open }">
      <div
        class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer relative"
        @click="open"
      >
        <IconInbox />

        <span
          v-if="hasUnreadNotifications"
          class="absolute top-0 right-0 flex size-2 mt-1 mr-1"
        >
          <span
            class="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75"
          ></span>
          <span
            class="relative inline-flex size-2 rounded-full bg-red-500"
          ></span>
        </span>
      </div>
    </template>
    <template #content="{ close }">
      <div class="w-64 rounded-2xl bg-white py-3 px-2 shadow-2xl text-xs">
        <div
          class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
        >

          <span class="flex items-center gap-x-2"><div class="size-1 min-w-1 rounded-full bg-red-500"></div>Tienen votos pendientes </span>
        </div>
        <div
          class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
        >
          <span class="flex items-center gap-x-2"><div class="size-1 min-w-1 rounded-full bg-red-500 "></div>Hay un nuevo comentario en la incidencia que reportaste </span>
        </div>
      </div>
    </template>
  </Dropdown>
</template>
<script setup>
import { ref, computed } from "vue";
import { useUserStore } from "/src/stores/useUserStore.js";

import IconInbox from "/src/components/icons/IconInbox.vue";
import Dropdown from "/src/components/Dropdown.vue";

defineOptions({
  name: "InboxNotifications",
});

//utils

const { user } = useUserStore();

const hasUnreadNotifications = computed(() => {
  //return user.notifications.some(notification => notification.read === false);
  return true;
});
</script>
