<template>
    <section class="bg-slate-800 flex flex-col items-center py-12">
        <div class=" max-w-[1280px] flex flex-col justify-center items-center py-6 mb-8">
            <div class="flex flex-col text-white justify-center items-center px-6">
                <span class="text-4xl font-semibold">Todo lo que tu comunidad necesita</span>
                <span class="text-lg mt-2">Gestión ágil, participación activa y total transparencia en un solo lugar.</span>
            </div>
        </div>
        <FeatureItemIncidence/>
        <FeatureItemSurvey/>
        <FeatureItemBookings/>
        <FeatureItemCommunication/>
        <FeatureItemDocs/>
       
    </section>   
</template>

<script setup >
    import { ref, shallowRef } from 'vue'
    import IconArrowRight from "/src/components/icons/IconArrowRight.vue"
    import FeatureItemIncidence from "/src/views/landing-modules/FeatureItemIncidence.vue"
    import FeatureItemSurvey from "/src/views/landing-modules/FeatureItemSurvey.vue"
    import FeatureItemBookings from "/src/views/landing-modules/FeatureItemBookings.vue"
    import FeatureItemCommunication from "/src/views/landing-modules/FeatureItemCommunication.vue"
    import FeatureItemDocs from "/src/views/landing-modules/FeatureItemDocs.vue"


    defineOptions ({
        name: 'FeaturesContent'
    });
  

</script>