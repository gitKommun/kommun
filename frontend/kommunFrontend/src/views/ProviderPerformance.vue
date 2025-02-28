<template>
  <div class="h-screen w-screen flex justify-center items-center">
    <div class="w-96 border border-slate-200 rounded-2xl p-4">
      <div
        class="text-slate-900 font-bold flex justify-between items-center mb-6"
      >
        <img alt="Kommun logo" class="h-6" src="@/assets/logo_kommun.svg" />
        <span>Solicitud de Actuación</span>
      </div>
      <div class="text-slate-500 text-sm">
        <p>
          La comunidad
          <span class="font-bold text-slate-900">"Mirador 2"</span> con
          dirección
          <span class="font-bold text-slate-900"
            >"C/Milan Nº45 pta2, Alfafar"</span
          >
          ha solicitado que realice una actuación para resolver una incidencia.
        </p>
      </div>
      <div class="py-3">
        <div class="text-xs uppercase text-slate-500">Incidencia:</div>
      </div>
      <div class="text-xs bg-yellow-50 text-yellow-600 rounded-xl p-3">
        <p>Titulo de la incidencia</p>
        <p>Descripción de la incidencia con texto largo</p>
        <p><span>Ubicación:</span> Dirección de la comunidad</p>
      </div>
      <div class="text-slate-500 text-sm mt-3">
        <p>Indique cuando puede atender la incidencia:</p>
      </div>
      <div class="flex flex-col gap-4 py-3">
        <div class="flex items-center gap-2 text-sm">
          <RadioButton
            v-model="term"
            inputId="inmediate"
            name="inmediate"
            value="inmediate"
          />
          <label for="inmediate">Inmediatamente</label>
        </div>
        <div class="flex items-center gap-2 text-sm">
          <RadioButton
            v-model="term"
            inputId="non_inmediate"
            name="non_inmediate"
            value="non_inmediate"
          />
          <label for="non_inmediate">En otro momento</label>
        </div>
      </div>
      <div class="py-3">
        <DatePicker 
            id="datepicker-12h" 
            v-model="term_time" 
            placeholder="Indica día y hora"
            showTime 
            hourFormat="24"
            variant="filled" 
            fluid 
            showIcon/>
      </div>
      <div class="py-4">
        <Button severity="contrast" label="Enviar" class="w-full" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
defineOptions({
  name: "ProviderPerformance",
});

const term = ref(null);
const term_time = ref(null);
</script>
