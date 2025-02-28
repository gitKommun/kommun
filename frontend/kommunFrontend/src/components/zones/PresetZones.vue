<template>
    <div class="border border-slate-200 rounded-2xl p-3 w-96 ">
        <h3 class="text-slate-950 font-semibold text-lg mb-3">Zonas más habituales</h3>
        <p class="text-sm text-slate-500 mb-3">Sabemos que todas las comunidades tiene zonas comunes, y estas son las más habituales, ¿quieres que las creemos ya por ti?</p>
        <div class="px-3 gap-y-2 mb-3">
            <div v-for="zone of popularZones" :key="zone.id" class="flex items-center gap-2 py-1">
            <Checkbox v-model="selectedZones" :inputId="zone.id" name="zone" :value="zone" />
            <label :for="zone.id">{{ zone.name }}</label>
        </div>
        </div>
        
        <Message severity="info" class="text-sm">Tranquilo, luego podras añadir todas las que necesites</Message>
        <div class="py-3">
            <Button severity="contrast" @click="sendRequest" label="Crear zonas" class="w-full"/>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
defineOptions({
    name: 'PresetZones'
})

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

//variables

const popularZones = ref([
    {
        id:1,
        name: 'Ascensores',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:2,
        name: 'Cubierta o tejado',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:3,
        name: 'Cuarto de basuras',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:4,
        name: 'Cuarto de contadores',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:5,
        name: 'Escaleras y rellanos',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        name: 'Fachada',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:6,
        name: 'Galerias',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:7,
        name: 'Patio interior',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:8,
        name: 'Portal',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    }
])
const selectedZones = ref([
    {
        id:1,
        name: 'Ascensores',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:2,
        name: 'Cubierta o tejado',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:3,
        name: 'Cuarto de basuras',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:4,
        name: 'Cuarto de contadores',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:5,
        name: 'Escaleras y rellanos',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        name: 'Fachada',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:6,
        name: 'Galerias',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:7,
        name: 'Patio interior',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    },
    {
        id:8,
        name: 'Portal',
        description: '-',
        reservable: false,
        reservation_duration: 0,
        time_unit: '',
    }
])


const emit = defineEmits(["update:items"]);
const sendRequest = async () => {
    if (selectedZones.value.length === 0) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Debes seleccionar al menos una zona',
            life: 3000
        });
        return;
    }
    
    try {
        let successCount = 0;
        let failedCount = 0;
        
        // Creación secuencial
        for (const zone of selectedZones.value) {
            try {
                await http.post(`common_areas/${user?.current_community?.community_id}/create/`, zone);
                successCount++;
            } catch (error) {
                console.error(`❌ Error en zona ${zone.name}:`, error);
                failedCount++;
            }
        }

        if (successCount > 0) {
            toast.add({
                severity: 'success',
                summary: 'Zonas creadas',
                detail: `Se han creado ${successCount} zonas correctamente${failedCount > 0 ? ` (${failedCount} fallidas)` : ''}`,
                life: 3000
            });
            emit("update:items", true);
        }

        if (failedCount > 0) {
            toast.add({
                severity: 'warn',
                summary: 'Algunas zonas no se pudieron crear',
                detail: `${failedCount} zonas no se pudieron crear`,
                life: 3000
            });
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error inesperado',
            detail: 'Ha ocurrido un error al crear las zonas',
            life: 3000
        });
        console.error('Error:', error);
    }
}
</script>