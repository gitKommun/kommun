<template>
    <div class="w-full flex flex-col items-center justify-center gap-4 py-12 px-6">
        <InputText v-model="form.name" placeholder="Nombre" variant="filled" class="w-full"/>
        <InputText v-model="form.email" placeholder="Email" variant="filled" class="w-full"/>
        <Textarea v-model="form.message" placeholder="Mensaje" variant="filled" class="w-full"/>
        <Button severity="contrast" size="large" class="w-full">Enviar</Button>
    </div>
</template>
<script setup>
import { ref } from 'vue';
defineOptions({
  name: "ContactForm",
});
const form = ref({
    name: '',
    email: '',
    message: '',
});
</script>