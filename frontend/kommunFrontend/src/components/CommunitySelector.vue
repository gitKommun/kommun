<template>
  <div class="w-full">
    <Select
      v-model="selected"
      :options="communities"
      optionLabel="community_name"
      variant="filled"
      placeholder="Seleccionar zona"
      class="w-full text-sm"
      filter
    />
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";

defineOptions({
  name: "CommunitySelector",
});
const props = defineProps({
  community: {
    type: Object,
  },
});
//utils
const http = useHttp();
const { user } = useUserStore();

//variables
const selected = ref(null);
const communities = ref([]);

const emit = defineEmits(["update:selected"]);

watch(selected, (newValue) => {
  if (newValue != props.community) {
    emit("update:selected", newValue);
  }
});


onMounted(() => {
  communities.value = user.available_communities;
  selected.value = props.community
});
</script>
