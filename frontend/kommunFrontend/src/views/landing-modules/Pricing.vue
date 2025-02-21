<template>
  <section class="flex flex-col items-center py-12">
    <div
      class="max-w-[1280px] flex flex-col justify-center items-center py-6 mb-8"
    >
      <h2
        class="text-4xl md:text-5xl font-bold text-slate-900 mb-8 text-center md:text-left"
      >
        Un solo plan que se adapta a ti
      </h2>
      <p class="max-w-[900px] text-slate-900 text-center">
        Gestiona todas tus comunidades con un plan flexible que crece contigo.
        Sin complicaciones, sin tarifas ocultas. Paga solo por las comunidades
        que administras y accede a todas las herramientas que necesitas para
        optimizar tu trabajo y mejorar la comunicación con los vecinos.
      </p>
    </div>
    <div class="max-w-[1280px] container">
      <div class="bg-white rounded-2xl p-3 w-full">
        <div class="w-full flex flex-col md:flex-row gap-3">
          <div
            class="w-full flex flex-col items-center bg-slate-50 rounded-2xl p-4 border border-slate-200"
          >
            <h3
              class="text-4xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-teal-400"
            >
              Mensual
            </h3>
            <h1
              class="text-6xl flex flex-col items-center font-bold text-center py-4"
            >
              2€
              <span class="text-sm text-slate-500 font-regular"
                >comunidad/mes</span
              >
            </h1>
            <Button severity="contrast" size="large">Selecionar</Button>
          </div>
          <div
            class="w-full flex flex-col items-center bg-slate-50 rounded-2xl p-4 border border-slate-200"
          >
            <h3
              class="text-4xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-400"
            >
              Anual
            </h3>
            <h1
              class="text-6xl flex flex-col items-center font-bold text-center py-4"
            >
              18€
              <span class="text-sm text-slate-500 font-regular"
                >comunidad/año</span
              >
            </h1>
            <Button severity="contrast" size="large">Selecionar</Button>
          </div>
        </div>

        <div class="w-full flex flex-wrap justify-center gap-3 py-8">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="flex  gap-3 w-full md:basis-[calc(33.333%-0.667rem)] bg-slate-50 rounded-xl p-3"
          >
            <div class="size-10 min-w-10 border bg-white border-slate-200 rounded-xl flex items-center justify-center">
              <component :is="feature.icon" class="text-indigo-500" />
            </div>
            <div class="flex flex-col pt-2">
              <span class="font-bold">{{ feature.name }}</span>
              <span class="text-sm text-slate-500">{{
                feature.description
              }}</span>
            </div>
          </div>
        </div>
        
      </div>
    </div>
  </section>
</template>
<script setup>
import { ref } from "vue";
import IconCircleCheck from "/src/components/icons/IconCircleCheck.vue";
import IconSpeakerphone from "/src/components/icons/IconSpeakerphone.vue";
import IconSurvey from "/src/components/icons/IconSurvey.vue";
import IconFolders from "/src/components/icons/IconFolders.vue";
import IconTool from "/src/components/icons/IconTool.vue";
import IconZones from "/src/components/icons/IconZones.vue";
import IconWorker from "/src/components/icons/IconWorker.vue";

defineOptions({
  name: "Pricinng",
});
//variables

const features = ref([
  {
    name: "Envio de comunicados",
    description: "Envía comunicados a todos los vecinos de la comunidad.",
    icon:IconSpeakerphone

  },
  {
    name: "Votaciones online",
    description: "Permite a los miembros votar en propuestas y decisiones.",
    icon:IconSurvey
  },
  {
    name: "Gestor documental",
    description: "Permite a los miembros compartir documentos y recursos.",
    icon:IconFolders
  },
  {
    name: "Gestor de incidencias",
    description: "Permite a los miembros reportar incidencias y problemas.",
    icon:IconTool
  },
  {
    name: "Reserva de espacios",
    description: "Permite a los miembros reservar espacios comunes.",
    icon:IconZones
  },
  //     {
  //     name: 'Presupuestos',
  //     description: 'Permite a los miembros crear presupuestos y solicitar financiación.',
  // },
  {
    name: "Libro de proveedores",
    description: "Directorio de proveedores de la comunidad.",
    icon:IconWorker
  },
]);
</script>
