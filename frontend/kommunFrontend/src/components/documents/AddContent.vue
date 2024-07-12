<template>
    <Dropdown strategy="fixed">
        <template #reference="{ open , isOpen }">
            <vs-button color="dark" @click="open">
                <IconPlus class="mr-2"/>
              Nuevo
            </vs-button>
        </template>
        <template #content>
          <!-- <transition
            enter-active-class="transition-all transition-slow ease-out overflow-hidden"
            leave-active-class="transition-all transition-slow ease-in overflow-hidden"
            enter-class="opacity-0 mt-6"
            enter-to-class="opacity-100 mt-0"
            leave-class="opacity-100 mt-0"
            leave-to-class="opacity-0 mt-6"
            mode="out-in"
          > -->
          <div class="bg-white w-56 rounded-xl p-3 shadow-2xl gap-y-2 flex flex-col">
            <AddNewFolder @update:folder="updateItems"/>
            <AddNewFile/>
          </div>

          <!-- </transition> -->

        </template>
      </Dropdown>
</template>
<script setup>
    import Dropdown from "/src/components/Dropdown.vue"
    import AddNewFolder from "/src/components/documents/AddNewFolder.vue";
    import AddNewFile from "/src/components/documents/AddNewFile.vue";
    import IconPlus from "/src/components/icons/IconPlus.vue";
    // options
    defineOptions({
    name: 'addContent',
    })

    const emit = defineEmits(['update:items']);
    const updateItems = () => {
        emit('update:items', true);
    }

</script>