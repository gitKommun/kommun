<template>
    <Dropdown strategy="fixed">
        <template #reference="{ open , isOpen }">
            <Button @click="open" severity="contrast" raised>
                <IconPlus/>
              Nuevo
            </Button>
        </template>
        <template #content>
          <div class="bg-white w-56 rounded-xl p-3 shadow-2xl gap-y-2 flex flex-col">
            <AddNewFolder @update:folder="updateItems" :selected="selected"/>
            <AddNewFile @update:document="updateItems" :selected="selected"/>
          </div>
        </template>
      </Dropdown>
</template>
<script setup>
    import { ref, shallowRef, computed } from 'vue'
    import Dropdown from "/src/components/Dropdown.vue"
    import AddNewFolder from "/src/components/documents/AddNewFolder.vue";
    import AddNewFile from "/src/components/documents/AddNewFile.vue";
    import IconPlus from "/src/components/icons/IconPlus.vue";
    // options
    defineOptions({
    name: 'addContent',
    })

const props = defineProps({
        selected: {
            type: Object,
            
        },
    });

    const emit = defineEmits(['update:items']);
    const updateItems = () => {
        emit('update:items', true);
    }

</script>