<template>
    <div class="container mx-auto pt-24">
        <Pricing />
    </div>
</template>
<script setup>
import Guests from '/src/layouts/Guests.vue';
import Pricing from '/src/views/landing-modules/Pricing.vue';
 defineOptions({
        name: 'Pricing',
        layout: Guests,
    });
</script>
