<template>
    <div class="p-4 border border-slate-200 rounded-2xl mb-3">
        <div class="flex items-center justify-between">
            <h3 class="text-slate-950 text-lg font-semibold"> Datos generales </h3>
        </div>
        <div class="gap-y-2">
            <div class="flex gap-x-3 py-4">
                <InputText v-model="form.name" placeholder="Nombre" class="w-full"/>
                <InputText v-model="form.surname" placeholder="Apellidos" class="w-full"/>
            </div>
            <div class="flex gap-x-3 py-4">
                <InputText v-model="form.email" placeholder="E-mail" class="w-full"/>
                <InputText v-model="form.phone" placeholder="Teléfono" class="w-full"/>
            </div>
            <div class="flex items-center py-4">
                <InputGroup>
                    <Select v-model="form.identificationType" :options="documentType" optionLabel="label" class="max-w-40" optionValue="value" placeholder="Selecciona..."/>
                    <InputText v-model="form.identificationNumber" placeholder="Número de identificación" class="max-w-64"/>
                </InputGroup>   
            </div>
            <div class="flex items-center py-4">
                <span class="min-w-10">
                    <ToggleSwitch v-model="form.allowSharing" />
                </span>
                <span class="ml-3"> Permitir que los otros propietarios tengan acesso a tus datos de contacto </span>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
import { useUserStore } from '/src/stores/useUserStore.js';

defineOptions({
    name: 'PersonalData',
})

const { user } = useUserStore();

//variables
const form = ref({
    name: user.name,
    surname: user.surnames,
    email: user.email,
    phone: user.phoneNumber,
    identificationNumber: user.documentID ?user.documentID : '',
    identificationType: user.documentType ?user.documentType : '',
    allowSharing:user.contactIsPublic   
})

 const documentType = ref([
        { label: 'DNI', value: 'DNI' },
        { label: 'NIE', value: 'NIE' },
        {label:'Pasaporte',value:'passport'}
    ])
</script>