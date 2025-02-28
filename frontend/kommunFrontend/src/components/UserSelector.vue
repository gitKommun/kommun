<template>
    <div class="w-full">
        <Select
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
const props = defineProps({
        owner: {
            type: Object
    },
        exclude: {
            type: Array,
            default: {}
        }
});
    //utils
    const http = useHttp();
    const { user } = useUserStore();    

//variables
    const selected = ref(null);
    const owners = ref([]);
    // const props = defineProps({
    //     property: {
    //         type: Object,
    //     },
    // });
    const emit = defineEmits(['update:selected']);

    watch(selected, (newValue) => {
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
