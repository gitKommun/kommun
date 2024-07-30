<template>
    <Fieldset legend="Datos generales">
            <div class="py-4">
                <InputText 
                    v-model="form.name" 
                    placeholder="Nombre de la comunidad" 
                    class="w-full"
                    variant="filled"/>
            </div>
            <!-- <div class="py-4">
                <InputText 
                    v-model="form.address" 
                    placeholder="Dirección" 
                    class="w-full"
                    variant="filled"/>
            </div> -->
            <div class="py-4 flex gap-x-3 ">
                <InputText 
                    v-model="form.province" 
                    placeholder="Provincia" 
                    class="w-full"
                    variant="filled"/>
                <InputText 
                    v-model="form.city" 
                    placeholder="Ciudad" 
                    class="w-full"
                    variant="filled"/>
            </div>
            <div class="py-4 flex gap-x-3 ">
                <InputText 
                    v-model="form.address" 
                    placeholder="Dirección" 
                    class="w-full"
                    variant="filled"/>
                <InputText 
                    v-model="form.postalCode" 
                    placeholder="Código postal" 
                    variant="filled"/>
            </div>
            
            <div class="py-4 flex gap-x-3 ">
                <InputText 
                    v-model="form.catastral_ref" 
                    placeholder="Referencia Catastral" variant="filled" />
                <InputText 
                    v-model="form.cif" 
                    placeholder="CIF" variant="filled" />
            </div>
            <div class="w-full flex justify-end">
                <Button
                    severity="contrast"
                    size="small"
                    :disabled="!hasChanged"
                    @click="updateCommunity()"
                    >
                    Guardar
                </Button>
            </div>
    </Fieldset>

</template>
<script setup>
    import { ref, watch, reactive } from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import { useToast } from 'primevue/usetoast';

    defineOptions({
        name: 'GeneralData'
    })
    //utils
    const http = useHttp();
    const { user } = useUserStore();
    const toast = useToast();

    // //variables
    const form = reactive({
        name: user?.current_community?.community_name,
        address: '',
        city:'',
        postalCode: '',
        cif: '',
        province: '',
        image: '',
        catastral_ref:''
    })

const hasChanged = ref(false);

watch(form, (newValue) => {
    hasChanged.value = true;
        //console.log('cambiando')
})

const updateCommunity = () => {
    try {
        const response = http.put(`communities/${user?.current_community?.community_id}/update/`, {
            ...form.value
        })
        toast.add({
            severity: 'success',
            summary: 'Ok',
            detail: 'Carpeta creada con exito',
            life: 3000
        });

    } catch (error) {
        toast.add({
            severity: 'danger',
            summary: 'Upps!! algo ha fallado',
            detail: error,
            life: 3000
        });
    }
}


</script>