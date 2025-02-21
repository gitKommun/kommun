<template>
  <div class="h-full w-full relative">
    <transition
      enter-from-class="-mt-16"
      enter-active-class="transitiona-all ease-in-out duration-150"
      move-class="transitiona-all bounce-transition duration-300"
    >
      <div
        class="w-full px-3 md:px-24 absolute top-0 mt-6 z-50 flex justify-center"
      >
        <header
          v-if="AppearMenu"
          class="w-full max-w-[1280px] text-slate-950 backdrop-blur bg-white/30 rounded-2xl border border-slate-200"
        >
          <div
            class="container mx-auto flex items-center justify-between py-2 px-4"
          >
            <RouterLink to="/">
              <span class="flex items-center">
                <img
                  alt="Kommun logo"
                  class="h-7"
                  src="@/assets/logo_kommun.svg"
                />
              </span>
            </RouterLink>
            <div class="hidden md:flex items-center space-x-4">
              <RouterLink to="/contact">
                <Button label="Contact" severity="contrast" text size="small" />
              </RouterLink>
              <RouterLink to="/pricing">
                <Button label="Pricing" severity="contrast" text size="small" />
              </RouterLink>
            </div>
            <div class="hidden md:flex items-center space-x-4">
              <router-link :to="{ name: 'login' }">
                <Button label="Login" severity="secondary" size="small">
                  Login
                  <span
                    class="w-5 h-5 text-slate-400 bg-slate-300 rounded text-xxs"
                    >L</span
                  >
                </Button>
              </router-link>
              <router-link :to="{ name: 'register' }">
                <Button
                  label="Registro"
                  severity="contrast"
                  raised
                  size="small"
                />
              </router-link>
            </div>
            <div class="md:hidden flex items-center">
              <Button outlined severity="contrast" @click="showMobileMenu">
                <IconClose v-if="showMenu" />
                <IconMenu v-else />
              </Button>
            </div>
          </div>
        </header>
      </div>
    </transition>
    <transition
      enter-active-class="transition-all transition-slow ease-out overflow-hidden"
      leave-active-class="transition-all transition-slow ease-in overflow-hidden"
      enter-class="opacity-0"
      enter-to-class="opacity-100"
      leave-class="opacity-100"
      leave-to-class="opacity-0"
      mode="out-in"
    >
      <div
        v-if="showMenu"
        class="absolute top-0 mt-16 z-10 md:hidden items-center justify-between flex w-full lg:flex lg:w-auto lg:order-1 bg-white rounded-2xl shadow-xl"
      >
        <div
          class="flex flex-col mt-4 font-medium w-full lg:flex-row lg:space-x-8 lg:mt-0 p-4 gap-y-3"
        >
          <RouterLink to="/contact">
            <Button label="Contact" severity="contrast" text size="small" class="w-full"/>
          </RouterLink>
          <RouterLink to="/pricing">
            <Button label="Pricing" severity="contrast" text size="small" class="w-full"/>
          </RouterLink>
          <router-link :to="{ name: 'login' }">
            <Button label="Login" severity="secondary" size="small" class="w-full"/>
          </router-link>
          <router-link :to="{ name: 'register' }">
            <Button label="Registro" severity="contrast" raised size="small" class="w-full"/>
          </router-link>
        </div>
      </div>
    </transition>
    <div class="flex justify-center">
      <slot />
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import IconMenu from "/src/components/icons/IconMenu.vue";
import IconClose from "/src/components/icons/IconClose.vue";
import { useRouter } from "vue-router";

defineOptions({
  name: "Guests",
});
//utils
const router = useRouter();
//variables
const showMenu = ref(false);
const AppearMenu = ref(false);

const showMobileMenu = () => {
  showMenu.value = !showMenu.value;
};

setTimeout(() => {
  AppearMenu.value = true;
}, 500);

//detectar si pulsa la tecla "L" para redirigir a la pagina de login
const handleKeyPress = (event) => {
  if (event.key === "l" || event.key === "L") {
    router.push("/login");
  }
};

// Agregar y remover el event listener
onMounted(() => {
  window.addEventListener("keydown", handleKeyPress);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyPress);
});
</script>
