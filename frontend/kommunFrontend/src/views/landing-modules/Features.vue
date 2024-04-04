<template>
    <section class="bg-slate-950 flex flex-col items-center py-12">
        <div class=" max-w-[1280px] flex flex-col justify-center items-center py-6 mb-8">
            <h2 class="text-2xl mb-3 text-white font-bold">Lorem ipsum dolor sit amet, consectetur adipiscing elit</h2>
            <p class="text-white">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        </div>
        <div class="max-w-[1280px] container mx-auto grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 px-4">
            <div 
                v-for="(feature, index) in features" :key="index" 
                class="flex flex-col bg-slate-900 hover:bg-slate-800 border border-slate-700 group rounded-2xl shadow-md p-4  hover:shadow-xl transition-all durations-300"
                >
                <div class="flex justify-between mb-4">
                    <div class="h-10 w-10  text-white flex justify-center items-center rounded-2xl"
                        :class="`bg-${feature.color}-500 shadow-${feature.color}-500`">
                        <Component :is="feature.icon" />
                    </div>
                    <Tag v-if="!feature.available" class="opacity-50">Soon</Tag>
                </div>
                <div class="pt-2">
                    <h3 class="font-semibold mb-2 text-white "
                        :class="`group-hover:text-${feature.color}-500`"
                    >{{ feature.title }}</h3>
                    <p class="text-sm text-slate-400">{{ feature.description }}</p>
                </div>
                <div class="text-xs text-slate-600 group-hover:text-cyan-500 mt-auto pt-8 flex justify-between items-center cursor-pointer">
                    <span>Read more</span>
                    <IconArrowRight class="opacity-0 group-hover:opacity-100 mr-6 group-hover:mr-0 transition-all duration-500"/>
                </div>
            </div>    
        </div>
    </section>   
</template>

<script setup >
    import { ref, shallowRef } from 'vue'
    import Guests from '/src/layouts/Guests.vue';
    import Tag from "/src/components/Tag.vue"
    import IconArrowRight from "/src/components/icons/IconArrowRight.vue"
    import IconUsers from "/src/components/icons/IconUsers.vue"
    import IconFinance from "/src/components/icons/IconFinance.vue"
    import IconSpeakerphone from "/src/components/icons/IconSpeakerphone.vue"
    import IconFolders from "/src/components/icons/IconFolders.vue"
    import IconTool from "/src/components/icons/IconTool.vue"
import IconSurvey from "/src/components/icons/IconSurvey.vue"
        import IconPin from "/src/components/icons/IconPin.vue"
    import IconWorker from "/src/components/icons/IconWorker.vue"

    defineOptions ({
        name: 'Features'
    });
  
const features = shallowRef([
    {
        title: 'Reuniones',
        description: 'Convoca y gestiona las reuniones de vecinos con eficacia y facilidad.',
        icon: IconUsers,
        available: true,
        color:'blue'
    }, {
        title: 'Finanzas',
        description: 'Controla los presupuestos y las finanzas de tu comunidad en tiempo real.',
        icon: IconFinance,
        available: true,
        color:'pink'
    }, {
        title: 'Incidencias',
        description: 'Recibe asistencia y soporte dedicado para garantizar el buen funcionamiento de tu comunidad.',
        icon: IconTool,
        available: true,
        color:'amber'
    }, {
        title: 'Documentación',
        description: 'Accede a todos los documentos importantes de tu comunidad cuando lo necesites.',
        icon: IconFolders,
        available: true,
        color:'lime'
    }, {
        title: 'Votaciones',
        description: 'Realiza votaciones online y obtén resultados instantáneos para tomar decisiones rápidas.',
        icon: IconSurvey,
        available: true,
        color:'violet'
    }, {
        title: 'Comunicación',
        description: 'Mantén a todos los vecinos informados y comunícate de manera efectiva.',
        icon: IconSpeakerphone,
        available: true,
        color:'teal'
    }, {
        title: 'Reserva de espacios',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        icon: IconPin,
        available: false,
        color:'fuchsia'
    },{
        title: 'Proveedores',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        icon: IconWorker,
        available: false,
        color:'orange'

    },
]);

</script>