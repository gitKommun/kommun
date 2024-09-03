<template>

    <Fieldset legend="Propiedades">
            <div class="w-full py-2 text-sm">
                <MeterGroup :value="value" />
            </div>
        
            <div class="md:columns-3 text-xs uppercase text-slate-500 mb-2">
                <div>Tipo</div>
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                    >
                    <div v-if="form.propertyTypes.length">Cantidad</div>
                </transition>
            </div>
            <div class="columns-1 md:columns-3  mb-2">
                <div class="flex items-center gap-x-2">
                    <Checkbox 
                        v-model="form.propertyTypes" 
                        inputId="apartment" 
                        value="apartment"
                        variant="filled"/> 
                    <label for="apartment">Apartamento</label> 
                </div>
                
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                >
                    <InputNumber 
                        v-if="form.propertyTypes.includes('apartment')"
                        v-model="form.apartmentAccount" 
                        placeholder="Nº de viviendas"  
                        showButtons
                        variant="filled"
                        />
                </transition>
            </div>
            <div class="columns-1 md:columns-3 mb-2">
                <div class="flex items-center gap-x-2">
                    <Checkbox 
                        v-model="form.propertyTypes" 
                        inputId="garage" 
                        value="garage"
                        variant="filled"/> 
                    <label for="garage">Plazas de aparcamiento</label> 
                </div>
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                >
                    <InputNumber 
                        v-if="form.propertyTypes.includes('garage')"
                        v-model="form.garageAccount" 
                        placeholder="Nº de plazas"
                        variant="filled"  
                        showButtons
                    />
                </transition>
            </div>
            <div class="columns-1 md:columns-3">
                <div class="flex items-center gap-x-2">
                    <Checkbox 
                        v-model="form.propertyTypes"
                        inputId="storageRoom"
                        value="storageRoom"
                        variant="filled"/> 
                    <label for="storageRoom">Trasteros</label> 
                </div>
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                >
                    <InputNumber 
                        v-if="form.propertyTypes.includes('storageRoom')"
                        v-model="form.storageRoomAccount" 
                        placeholder="Nº de trasteros" 
                        variant="filled" 
                        showButtons
                    />
                </transition>
            </div>
        
    </Fieldset>

</template>
<script setup>
    import { ref } from 'vue'
    import { useHttp } from '/src/composables/useHttp.js'; 
    import { useUserStore } from '/src/stores/useUserStore.js';

    defineOptions({
        name: 'Properties'
    })

    //variables
    const form = ref({
        propertyTypes: [],
        apartmentAccount: null,
        garageAccount: null,
        storageRoomAccount: null,    
    })

    //instancia API
    const http = useHttp();
    const { user } = useUserStore();

const value = ref([
    { label: 'Residencial', color: '#34d399', value: 56 },
    { label: 'Almacén-Estacionamiento', color: '#fbbf24', value: 24 },
    { label: 'Oficina', color: '#60a5fa', value: 8 },
    { label: 'Industria', color: '#c084fc', value: 10 }
]);


</script>