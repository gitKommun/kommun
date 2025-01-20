<template>
  <div class="h-screen w-screen bg-slate-100 flex flex-col md:flex-row">
    <!-- menu-aside -->
    <div
      class="hidden md:flex flex-col items-center transition-all duration-300 bounce-transition py-6 pl-3"
      :class="isAsideOpen ? 'md:w-64' : 'md:w-0'"
    >
      <img
        v-if="isAsideOpen"
        alt="Kommun logo"
        key="logo"
        class="h-16"
        src="@/assets/logo_kommun.svg"
      />
      <img
        v-else
        alt="Kommun logo"
        key="iso"
        class="h-16"
        src="@/assets/iso_kommun.svg"
      />
      <div class="w-full h-full flex flex-col items-center justify-center">
        <div
          class="w-full flex-1 min-h-0 gap-y-1 flex flex-col items-center pt-8 overflow-y-scroll"
        >
          <div class="w-full  bg-white/50 p-2 rounded-2xl">
            <div class="flex items-center gap-x-2 border-b border-slate-100 pb-2">
              <div class="h-9 w-9 bg-white border border-slate-100 flex items-center justify-center rounded-xl">
                <IconSpaces class="text-indigo-500"/>
              </div>
              <span class="text-sm font-semibold truncate items-center">Comunidad</span>
            </div>
            <div class="px-1 py-2 flex flex-col gap-y-2 ">
              <p class="text-sm truncate">{{ currentCommunnityName }}</p>
              <span class="text-xs text-slate-500 truncate">Dirección</span>
            </div>
            <div class="flex justify-end">
              <router-link
              to="/communities"
              class="text-indigo-500 flex items-center hover:text-indigo-700 hover:bg-indigo-100 transition-all duration-300 rounded-lg px-2 py-1 text-xs"
              >
                <span>Cambiar</span>
                <IconChevronRight class="scale-75 ml-1" />
              </router-link>
            </div>
          </div>
          <div class="w-full border-t border-slate-200 my-3"></div>
          <router-link
            v-for="(section, index) in setMenu"
            :key="'#' + index"
            :to="section.to"
            class="h-10 flex items-center rounded-xl cursor pointer group transition-all duration-300"
            :class="[
              isAsideOpen ? 'w-full pl-4 gap-4' : 'w-10 justify-center',
              {
                'bg-white': isLinkActive(section.to),
                'hover:bg-slate-200': !isLinkActive(section.to),
              },
            ]"
          >
            <component
              :is="section.icon"
              :class="[
                isLinkActive(section.to) ? 'text-slate-950' : 'text-slate-400',
              ]"
            />
            <span
              v-if="isAsideOpen"
              class="text-sm"
              :class="
                isLinkActive(section.to) ? 'font-semibold' : 'font-regular'
              "
            >
              {{ section.title }}
            </span>
          </router-link>
        </div>
      </div>
    </div>
    <!-- menu-aside -->
    <!-- menu-mobile -->
    <div
      class="absolute top-0 w-full h-full flex flex-col bg-white/75 z-100 backdrop-blur p-4 md:hidden transition-all duration-300"
      :class="showMenuMobile ? 'translate-x-0' : '-translate-x-full '"
    >
      <div class="flex justify-between items-center h-16 px-4">
        <img
          alt="Kommun logo"
          key="logo"
          class="h-16"
          src="@/assets/logo_kommun.svg"
        />
        <IconClose @click="showMenuMobile = false" />
      </div>
      <div class="flex items-center justify-center flex-1 min-h-0">
        <div class="w-full flex flex-col items-start px-12 gap-y-2 -mt-16">
          <div class="w-full  bg-white/50 p-2 rounded-2xl border border-slate-200">
            <div class="flex items-center gap-x-2 border-b border-slate-100 pb-2">
              <div class="h-9 w-9 bg-white border border-slate-100 flex items-center justify-center rounded-xl">
                <IconSpaces class="text-indigo-500"/>
              </div>
              <span class="text-sm font-semibold truncate items-center">Comunidad</span>
            </div>
            <div class="px-1 py-2 flex flex-col gap-y-2 ">
              <p class="text-sm truncate">{{ currentCommunnityName }}</p>
              <span class="text-xs text-slate-500 truncate">Dirección</span>
            </div>
            <div class="flex justify-end">
              <router-link
              to="/communities"
              class="text-indigo-500 flex items-center hover:text-indigo-700 w-full md:w-auto justify-center bg-indigo-100 md:bg-transparent hover:bg-indigo-100 transition-all duration-300 rounded-lg px-2 py-1 text-xs"
              >
                <span>Cambiar</span>
                <IconChevronRight class="scale-75 ml-1" />
              </router-link>
            </div>
          </div>
          <div class="w-full border-t border-slate-200 my-3"></div>
          <router-link
            v-for="(section, index) in setMenu"
            :key="'#' + index"
            :to="section.to"
            class="h-10 w-full px-3 flex flex-none items-center rounded-xl cursor pointer transition-all duration-300"
            :class="[
              isLinkActive(section.to)
                ? 'bg-violet-500 text-white'
                : 'hover:bg-slate-200 ',
            ]"
          >
            <component
              :is="section.icon"
              class="mr-3 flex-none"
              :class="[
                isLinkActive(section.to) ? `text-white` : 'text-slate-400',
              ]"
            />
            <span class="text-sm">{{ section.title }} </span>
          </router-link>
        </div>
      </div>
    </div>
    <!-- menu-mobile -->
    <!-- Content -->
    <div class="w-full flex-1 min-w-0 p-3">
      <div
        class="bg-white rounded-2xl shadow-xl h-full w-full flex flex-col overflow-hidden"
      >
        <div class="w-full flex items-center justify-between min-h-12 pl-2">
          <div class="flex items-center gap-x-3">
            <span
              class="h-8 w-8 rounded-xl hover:bg-slate-100 text-slate-400 hidden md:flex items-center justify-center"
              @click="asideToogle"
            >
              <IconAsideExpand v-if="isAsideOpen" />
              <IconAsideCollapsed v-else />
            </span>
            <span
              class="flex items-center gap-x-1 pl-2 md:hidden"
              @click="toggleMenuMobile"
            >
              <IconMenu class="h-6 w-6" />
            </span>
            <span
              class="text-slate-950 text-xl font-bold truncate items-center"
            >
              {{ getRouteName }}
              <span class="text-slate-500 text-sm font-medium"
                >| {{ user?.current_community?.community_name }}</span
              >
            </span>
          </div>
          <div class="pr-3 flex items-center gap-x-2">
            <div class="h-8 w-8 rounded-xl hover:bg-slate-100 flex items-center justify-center" >
              <IconInbox/>
            </div>
            <Dropdown strategy="fixed">
              <template #reference="{ open }">
                <div
                  class="rounded-xl hover:bg-slate-100 items-center flex flex-none transition-all duration-300 cursor-pointer"
                  @click="open"
                >
                  <CustomAvatar :name="getName()" :size="'small'" />
                </div>
              </template>

              <template #content="{ close }">
                <div
                  class="w-48 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm"
                >
                  <div class="">
                    <span class="text-sm font-semibold ml-3">{{
                      user?.name + " " + user?.surnames
                    }}</span>
                  </div>
                  <router-link to="/profile">
                    <div
                      class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
                    >
                      <IconUserAccount class="scale-75" />
                      <span>Mi perfil</span>
                    </div>
                  </router-link>

                  <div
                    class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                    @click="logout"
                  >
                    <IconLogout class="scale-75" />
                    <span>Cerrar Sesión</span>
                  </div>
                </div>
              </template>
            </Dropdown>
          </div>
        </div>
        <slot class="min-h-0 flex-1 flex flex-col relative" />
      </div>
    </div>
    <!-- Content -->
  </div>
</template>
<script setup>
import { ref, shallowRef, computed, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useHttp } from "/src/composables/useHttp.js";
import IconAsideCollapsed from "/src/components/icons/IconAsideCollapsed.vue";
import IconAsideExpand from "/src/components/icons/IconAsideExpand.vue";
import IconUsers from "/src/components/icons/IconUsers.vue";
import IconMenu from "/src/components/icons/IconMenu.vue";
import IconSpeakerphone from "/src/components/icons/IconSpeakerphone.vue";
import IconFolders from "/src/components/icons/IconFolders.vue";
import IconTool from "/src/components/icons/IconTool.vue";
import IconSurvey from "/src/components/icons/IconSurvey.vue";
import IconInbox from "/src/components/icons/IconInbox.vue";
import IconClose from "/src/components/icons/IconClose.vue";
import IconZones from "/src/components/icons/IconZones.vue";
import IconChevronRight from "/src/components/icons/IconChevronRight.vue";
import IconKey from "/src/components/icons/IconKey.vue";
import IconLogout from "/src/components/icons/IconLogout.vue";
import IconBell from "/src/components/icons/IconBell.vue";
import IconUserAccount from "/src/components/icons/IconUserAccount.vue";
import IconSpaces from "/src/components/icons/IconSpaces.vue";
import Dropdown from "/src/components/Dropdown.vue";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";
import CustomAvatar from "/src/components/CustomAvatar.vue";
defineOptions({
  name: "home",
});

// utils
const toast = useToast();
const http = useHttp();
const { user } = useUserStore();

//logout
const logoutLoading = ref(false);
const logout = async () => {
  logoutLoading.value = true;
  try {
    await http.post(`members/logout/`);
    logoutLoading.value = false;
    window.location.reload();
  } catch (error) {
    toast.add({
      severity: "danger",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
    loginLoading.value = false;
  }
};

//iniciales avatar
const getName = () => {
  const fullName = user?.name + " " + user?.surnames;
  return fullName;
};

//collapse expand vertical menu
const isAsideOpen = ref(false);

//guardar carpeta en localStorage
watch(isAsideOpen, (newValue) => {
  localStorage.setItem("asideStatus", newValue);
});

onMounted(() => {
  isAsideOpen.value = localStorage.getItem("asideStatus");
});

const asideToogle = () => {
  isAsideOpen.value = !isAsideOpen.value;
};



const showMenuMobile = ref(false);

const toggleMenuMobile = () => {
  showMenuMobile.value = !showMenuMobile.value;
};

//get active route
const route = useRoute();
const isLinkActive = (routeName) => {
  return route.fullPath === routeName; // Compara el to del enlace con la fullPath del objeto route
};
const routeName = {
  communities: "Comunidades",
  properties: "Propiedades",
  surveys: "Votaciones",
  incidences: "Incidencias",
  owners: "Propietarios",
  bookings: "Reservas",
  documents: "Documentos",
  communication: "Foro",
  settings: "Configuración",
  zones: "Zonas comunes",
};
const getRouteName = computed(() => {
  return routeName[route.name];
});

const currentCommunnityName = computed(() => {
  return user?.current_community.community_name;
});

const adminFeatures = shallowRef([

  {
    title: "Propiedades",
    icon: IconKey,
    available: true,
    to: "/properties",
  },
  {
    title: "Propietarios",
    icon: IconUsers,
    available: true,
    to: "/owners",
  },
  {
    title: "Zonas comunes",
    icon: IconZones,
    available: true,
    to: "/zones",
  },
  {
    title: "Incidencias",
    icon: IconTool,
    available: true,
    to: "/incidences",
  },
  {
    title: "Documentación",
    icon: IconFolders,
    available: true,
    to: "/documents",
  },
  {
    title: "Votaciones",
    icon: IconSurvey,
    available: true,
    to: "/surveys",
  },
  {
    title: "Foro",
    icon: IconSpeakerphone,
    available: true,
    to: "/communication",
  },
  
]);

const userFeatures = shallowRef([
  {
    title: "Incidencias",
    icon: IconTool,
    available: true,
    to: "/incidences",
  },
]);

const isAdmin = computed(() => {
  if (user?.current_community?.community_role === "admin") {
    return true;
  }
  return false;
});

const setMenu = computed(() => {
  if (isAdmin) {
    return adminFeatures.value;
  }
  return userFeatures.value;
});
</script>
<style>
.smoth {
  scroll-behavior: smooth;
}
/* .noScroll{
    scrollbar-gutter: stable;
} */
::-webkit-scrollbar {
  display: none;
}
</style>
