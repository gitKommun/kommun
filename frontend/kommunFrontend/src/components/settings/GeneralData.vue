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
               {{ props.id }} 
                <Button
                    severity="contrast"
                    size="small"
                    
                    @click="updateCommunity()"
                    >
                    Guardar
                </Button>
            </div>
    </Fieldset>

</template>
<script setup>
    import { ref, watch, reactive, onMounted, shallowReactive} from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';
    import { useToast } from 'primevue/usetoast';

    defineOptions({
        name: 'GeneralData'
    })

    const props = defineProps({
        community: {
            type: Object,
        },
    });
    //utils
    const http = useHttp();
    const { user } = useUserStore();
    const toast = useToast();

    // //variables
    const form = ref({
        name: '',
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

watch(
  () => props.community,
  (newCommunity) => {
    form.value.name = props.community.nameCommunity || ''
    form.value.address = props.community.address || ''
    form.value.city = props.community.city || ''
    form.value.postalCode = props.community.postal_code || ''
    // Puedes inicializar otros campos según sea necesario
  },
  { immediate: true } // Ejecutar el watcher inmediatamente
)



const updateCommunity = () => {
    try {
        const response = http.put(`communities/${props.community.IDcommunity}/update/`, {
            //...form.value
            nameCommunity: form.value.name,
            address: form.value.address,
            city: form.value.city,
            postal_code:form.value.postalCode
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