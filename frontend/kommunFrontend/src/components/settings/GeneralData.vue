<template>
    <Fieldset legend="Datos generales">
            <div class="py-4">
                <InputText 
                    v-model="form.name" 
                    placeholder="Nombre de la comunidad" 
                    class="w-full"
                    variant="filled"/>
            </div>
            <div class="py-4">
                <InputText 
                    v-model="form.address" 
                    placeholder="Dirección" 
                    class="w-full"
                    variant="filled"/>
            </div>
            <div class="py-4 flex gap-x-3 ">
                <InputText 
                    v-model="form.city" 
                    placeholder="Ciudad" 
                    class="w-full"
                    variant="filled"/>
                <InputText 
                    v-model="form.postalCode" 
                    placeholder="Código postal" 
                    class="w-full"
                    variant="filled"/>
            </div>
            <div class="py-4 flex gap-x-3 ">
                <InputText 
                    v-model="form.cif" 
                    placeholder="CIF" variant="filled" />
            </div>
    </Fieldset>

</template>
<script setup>
    import { ref } from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';

    defineOptions({
        name: 'GeneralData'
    })
    //instancia API
    const http = useHttp();
    //user store
    const { user } = useUserStore();

    //variables
    const form = ref({
        name: user?.current_community?.community_name,
        address: '',
        city:'',
        postalCode: '',
        cif: '',
    })

    


</script>