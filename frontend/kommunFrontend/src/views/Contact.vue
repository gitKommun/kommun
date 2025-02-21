<template>
  <div class="container mx-auto flex justify-center pt-24">
    <div class="w-full max-w-[1280px] flex flex-col md:flex-row justify-center items-center py-6 mb-8">
      <div class="w-full md:w-1/2 p-3">
        <h2
          class="text-2xl md:text-3xl font-bold text-slate-900 mb-8 text-center md:text-left px-6"
        >
          ¿Tienes preguntas? Escríbenos
        </h2>
        <p class="max-w-[900px] text-slate-900 text-center md:text-left px-6">
          Déjanos tu consulta a través del formulario y te responderemos lo antes posible. Estamos aquí para ayudarte a gestionar tu comunidad de la mejor manera.
        </p>
        <ContactForm />
      </div>
      <div class="w-full md:w-1/2 p-3 h-full">
        <div class="h-full w-full bg-gradient-to-tr from-blue-300 to-teal-200 rounded-2xl p-3">img</div>
      </div>
    </div>
  </div>
</template>
<script setup>
import Guests from "/src/layouts/Guests.vue";
import ContactForm from "/src/views/landing-modules/ContactForm.vue";
defineOptions({
  name: "Contact",
  layout: Guests,
});
</script>
