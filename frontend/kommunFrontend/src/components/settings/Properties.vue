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
                <vs-checkbox v-model="form.propertyTypes" color="success" value="apartment"> Viviendas </vs-checkbox>
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                >
                    <vs-input 
                        v-if="form.propertyTypes.includes('apartment')"
                        v-model="form.apartmentAccount" 
                        placeholder="Nº de viviendas"  
                        type="number"
                        />
                </transition>
            </div>
            <div class="columns-1 md:columns-3 mb-2">
                <vs-checkbox v-model="form.propertyTypes" color="success" value="garage" > Plazas de aparcamiento </vs-checkbox>
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                >
                    <vs-input 
                        v-if="form.propertyTypes.includes('garage')"
                        v-model="form.garageAccount" 
                        placeholder="Nº de plazas"  
                        type="number"
                        class="w-12"
                    />
                </transition>
            </div>
            <div class="columns-1 md:columns-3">
                <vs-checkbox v-model="form.propertyTypes" color="success" value="storageRoom"> Trasteros </vs-checkbox>
                <transition
                    enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                    leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                    enter-class="opacity-0"
                    enter-to-class="opacity-100"
                    leave-class="opacity-100"
                    leave-to-class="opacity-0"
                    mode="out-in"
                >
                    <vs-input 
                        v-if="form.propertyTypes.includes('storageRoom')"
                        v-model="form.storageRoomAccount" 
                        placeholder="Nº de trasteros"  
                        type="number" 
                        />
                </transition>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { ref, shallowRef } from 'vue'
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