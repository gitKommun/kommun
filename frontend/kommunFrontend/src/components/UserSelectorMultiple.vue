<template>
    <div class="w-full">
        <MultiSelect
        v-model="selected"
        :options="owners"
        optionLabel="full_name"
        variant="filled"
        placeholder="Seleccionar propietario"
        class="w-full"
        filter
    />
    </div>
    
</template>
<script setup>
import { ref, onMounted, watch} from 'vue'
import { useHttp } from '/src/composables/useHttp.js';
import { useUserStore } from '/src/stores/useUserStore.js'; 

defineOptions({
    name: 'UserSelector',
})
    //utils
    const http = useHttp();
    const { user } = useUserStore();    

//variables
    const owners = ref([]);
    const selected = ref([]);

    // const props = defineProps({
    //     property: {
    //         type: Object,
    //     },
    // });
    const emit = defineEmits(['update:selected']);

    watch(selected, (newValue) => {
        // console.log('nv',newValue)
        emit('update:selected', newValue);   
    })


    const getOwners = async () => {
        try {

        const response = await http.get(`communities/${user?.current_community?.community_id}/neighbors/`);
            owners.value = response.data
        
        } catch (error) {
            console.log(error)
        }
    }

    onMounted(() => {
        getOwners()
    });


</script>
