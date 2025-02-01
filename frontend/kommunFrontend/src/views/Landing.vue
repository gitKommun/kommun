<template>
    <div class="h-full w-full">
        <Cover/>
        <MultyCommunity/>
        <DesignedFor/>
        <!-- <FeaturesContent/> -->
        <!-- <Cover/>
        <Features/> -->
        <Pricing/>
    </div>   
</template>
<script setup >
import Guests from '/src/layouts/Guests.vue';
// import Features from '/src/views/landing-modules/Features.vue';
// import FeaturesContent from '/src/views/landing-modules/FeaturesContent.vue';
import Cover from '/src/views/landing-modules/Cover.vue';
import MultyCommunity from '/src/views/landing-modules/MultyCommunity.vue';
import DesignedFor from '/src/views/landing-modules/DesignedFor.vue';
import Pricing from '/src/views/landing-modules/Pricing.vue';
import { ref } from 'vue';
        defineOptions ({
            name: 'Landing',
            layout: Guests,
        });
</script>