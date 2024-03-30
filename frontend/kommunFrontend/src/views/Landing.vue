<template>
    <div class="h-full w-full  pt-16 ">
        <Cover/>
        <Features/>
        <Pricing/>
    </div>   
</template>
<script setup >
import Guests from '/src/layouts/Guests.vue';
import Features from '/src/views/landing-modules/Features.vue';
import Cover from '/src/views/landing-modules/Cover.vue';
import Pricing from '/src/views/landing-modules/Pricing.vue';
import { ref } from 'vue';
        defineOptions ({
            name: 'Landing',
            layout: Guests,
        });
</script>