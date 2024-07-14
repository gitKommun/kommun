<template>
    <div class="p-4 border border-slate-200 rounded-2xl mb-3">
        <div class="flex items-center justify-between">
            <h3 class="text-slate-950 text-lg font-semibold">Propiedades</h3>
        </div>
        <div class="gap-y-2 pt-3">
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
                    <Checkbox v-model="form.propertyTypes" inputId="apartment" value="apartment"/> 
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
                        />
                </transition>
            </div>
            <div class="columns-1 md:columns-3 mb-2">
                <div class="flex items-center gap-x-2">
                    <Checkbox v-model="form.propertyTypes" inputId="garage" value="garage"/> 
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
                        showButtons
                    />
                </transition>
            </div>
            <div class="columns-1 md:columns-3">
                <div class="flex items-center gap-x-2">
                    <Checkbox v-model="form.propertyTypes" inputId="storageRoom" value="storageRoom"/> 
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
                        showButtons
                    />
                </transition>
            </div>
        </div>
    </div>
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
    //user store
    const { user } = useUserStore();


</script>