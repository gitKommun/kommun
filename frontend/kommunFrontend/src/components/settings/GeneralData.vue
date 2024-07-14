<template>
    <div class="p-4 border border-slate-200 rounded-2xl mb-3">
        <div class="flex items-center justify-between">
            <h3 class="text-slate-950 text-lg font-semibold"> Datos generales</h3>
        </div>
        <div class="gap-y-2">
            <div class="py-4">
                <InputText v-model="form.name" placeholder="Nombre de la comunidad" class="w-full"/>
            </div>
            <div class="py-4">
                <InputText v-model="form.address" placeholder="Dirección" class="w-full"/>
            </div>
            <div class="py-4 flex gap-x-3 ">
                <InputText v-model="form.city" placeholder="Ciudad" class="w-full"/>
                <InputText v-model="form.postalCode" placeholder="Código postal" class="w-full"/>
            </div>
            <div class="py-4 flex gap-x-3 ">
                <InputText v-model="form.cif" placeholder="CIF" label-float />
            </div>
        </div>
    </div>
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
        name: user?.communities[0]?.community_name,
        address: '',
        city:'',
        postalCode: '',
        cif: '',
    })

    


</script>