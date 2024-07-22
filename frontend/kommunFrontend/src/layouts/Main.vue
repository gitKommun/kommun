<template>
  <div class="h-screen w-screen bg-slate-100 flex flex-col md:flex-row">
    <!-- menu-aside -->
    <div class=" hidden md:flex flex-col items-center transition-all duration-300 bounce-transition py-6 pl-3"
      :class="isAsideOpen?'md:w-64':'md:w-24'">

        <img v-if="isAsideOpen" alt="Kommun logo" key="logo" class="h-16" src="@/assets/logo_kommun.svg"  />
        <img v-else alt="Kommun logo" key="iso" class="h-16" src="@/assets/iso_kommun.svg"  />
      <div class=" w-full h-full flex flex-col items-center justify-center">
        <div class="w-full flex-1 min-h-0 gap-y-3 flex flex-col items-center pt-8 overflow-y-scroll">
            <router-link 
                v-for="(section, index) in setMenu" 
                :key="'#'+index" 
                :to="section.to" 
                class="h-10 flex  items-center rounded-xl cursor pointer group transition-all duration-300"
                :class="[isAsideOpen?'w-full pl-4 gap-4':'w-10 justify-center',{'bg-white':isLinkActive(section.to),'hover:bg-slate-200':!isLinkActive(section.to)}]"
                >
                    <component 
                        :is="section.icon"
                        
                        :class="[isLinkActive(section.to)?`text-${section.color}-500`:'text-slate-400']"
                        />
                    <span v-if="isAsideOpen" class="text-sm" >{{section.title}}</span>

            </router-link>
        
        </div>
        <div class="w-full gap-y-3 flex flex-col items-center pt-4 border-t border-slate-20">
            <router-link
              v-if="isAdmin" 
              class="h-10 flex  items-center hover:bg-slate-200 rounded-xl cursor pointer"
              :class="isAsideOpen?'w-full pl-4 gap-4':'w-10 justify-center'"
              to="/settings"
            >
              <IconSettings class="text-slate-400"/>
              <span v-if="isAsideOpen" class="text-sm">Settings</span>
            
            </router-link>
            <div class="h-10 flex  items-center rounded-xl cursor pointer"
              :class="isAsideOpen?'w-full pl-2 gap-4':'w-10 justify-center'"
            >
              <Dropdown strategy="fixed">
                <template #reference="{ open }">
                    <div 
                        class="rounded-xl hover:bg-slate-100 items-center flex flex-none transition-all duration-300 cursor-pointer "
                        @click="open"
                    >
                        <Avatar :label="getInitials()" size="large" shape="circle"/>
                        <span v-if="isAsideOpen" class="text-sm font-semibold ml-3">Jane Smith</span>  
                    </div>
                </template>

                <template #content="{ close }">
                    <div class="w-48 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm">
                        <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                          >
                            <IconBell class="scale-75"/>
                            <span>Notificaciones</span>
                        </div>
                        <router-link to="/profile">
                          <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                        >
                            <IconUserAccount class="scale-75"/>
                            <span>Mi perfil</span>
                        </div>
                        </router-link>
                        
                        <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                            @click="logout"
                            >
                            <IconLogout class="scale-75"/>
                            <span>Cerrar Sesión</span>
                        </div>
                    </div>
                </template>
            </Dropdown>   
            </div>
      
        </div>
      </div>
    </div>
    <!-- menu-aside -->
    <!-- menu-top -->
    <div class="flex md:hidden w-full flex-col ">
      <div class="w-full flex justify-between items-center px-3">
          <img alt="Kommun logo" key="logo" class="h-16" src="@/assets/logo_kommun.svg"  />
          <Dropdown strategy="fixed">
                <template #reference="{ open }">
                    <div 
                        class="rounded-xl hover:bg-slate-100 items-center flex flex-none transition-all duration-300 cursor-pointer "
                        @click="open"
                    >
                        <Avatar :label="getInitials()" size="large" shape="circle"/>
                    </div>
                </template>

                <template #content="{ close }">
                    <div class="w-48 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm">
                        <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                          >
                            <IconBell class="scale-75"/>
                            <span>Notificaciones</span>
                        </div>
                        <router-link to="/profile">
                          <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300  cursor-pointer"
                        >
                            <IconUserAccount class="scale-75"/>
                            <span>Mi perfil</span>
                        </div>
                        </router-link>
                        
                        <div class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                            @click="logout"
                            >
                            <IconLogout class="scale-75"/>
                            <span>Cerrar Sesión</span>
                        </div>
                    </div>
                </template>
            </Dropdown>   
      </div>
      <div class="flex w-full h-10 px-3 gap-x-3">
        <div class="flex justify-center items-center h-10 w-10 rounded-2xl hover:bg-slate-200 transition-all duration-300"
          @click="panToLeft"
        >
          <IconChevronLeft/>
        </div>
        <div ref="wrapper" class="flex-1 min-w-0  flex overflow-x-scroll smoth">
          <div ref="content" class="h-full w-auto gap-x-3 whitespace-nowrap flex ">
            <router-link 
                v-for="(section, index) in setMenu" 
                :key="'#'+index" 
                :to="section.to" 
                class="h-10  px-3  flex flex-none items-center   rounded-xl cursor pointer 
              transition-all duration-300"
              :class="[isLinkActive(section.to)?'bg-white ':'hover:bg-slate-200 ']"
              >
              <component 
                    :is="section.icon" 
                    class="mr-3 flex-none"
                    :class="[isLinkActive(section.to)?`text-${section.color}-500`:'text-slate-400']"/>
              <span class="text-sm">{{section.title}} </span>
            </router-link> 
          </div>
               
        </div>
        <div class="flex justify-center items-center h-10 w-10 rounded-2xl hover:bg-slate-200 transition-all duration-300"
          @click="panToRight"
        >
          <IconChevronRight/>
        </div>
      </div>
      
    </div>
    <!-- menu-top -->
    <div class="w-full  flex-1 min-w-0 p-3">
      <div class="bg-white rounded-2xl shadow-xl h-full w-full relative overflow-hidden">
        <div class="absolute z-50 ml-2 mt-7 h-8 w-8 rounded-xl hover:bg-slate-100 text-slate-400 hidden md:flex items-center justify-center" @click="asideToogle">
          <transition
          enter-active-class="transition-all transition-slow ease-out overflow-hidden"
          leave-active-class="transition-all transition-slow ease-in overflow-hidden"
          enter-class="opacity-0"
          enter-to-class="opacity-100"
          leave-class="opacity-100"
          leave-to-class="opacity-0"
          mode="out-in"
        >
          <IconAsideExpand v-if="isAsideOpen"/>
          <IconAsideCollapsed v-else/>
          </transition>
        </div>

        <slot/>
      </div>
    </div>

  </div>
  
</template>
<script setup>
import { ref, shallowRef, computed } from 'vue'
import { useRoute } from 'vue-router';
import { useHttp } from '/src/composables/useHttp.js'; 
import IconAsideCollapsed from "/src/components/icons/IconAsideCollapsed.vue"
import IconAsideExpand from "/src/components/icons/IconAsideExpand.vue"
  import IconUsers from "/src/components/icons/IconUsers.vue"
    import IconFinance from "/src/components/icons/IconFinance.vue"
    import IconSpeakerphone from "/src/components/icons/IconSpeakerphone.vue"
    import IconFolders from "/src/components/icons/IconFolders.vue"
    import IconTool from "/src/components/icons/IconTool.vue"
import IconSurvey from "/src/components/icons/IconSurvey.vue"
    import IconPin from "/src/components/icons/IconPin.vue"
import IconWorker from "/src/components/icons/IconWorker.vue"
import IconSettings from "/src/components/icons/IconSettings.vue"
import IconChevronRight from "/src/components/icons/IconChevronRight.vue"
import IconChevronLeft from "/src/components/icons/IconChevronLeft.vue"
import IconBuilding from "/src/components/icons/IconBuilding.vue"
import IconLogout from "/src/components/icons/IconLogout.vue"
import IconBell from "/src/components/icons/IconBell.vue"
import IconUserAccount from "/src/components/icons/IconUserAccount.vue"
import Dropdown from "/src/components/Dropdown.vue"
import { useUserStore } from '/src/stores/useUserStore.js';
import { useToast } from 'primevue/usetoast';
defineOptions({
  name:'home'
})

// uses
        //use toast
const toast = useToast();
    
//instancia API
const http = useHttp();
//user store
const { user } = useUserStore();

//logout
const logoutLoading = ref(false);

const logout = async () => {
  logoutLoading.value = true
  try {
    await http.post(`members/logout/`)
    logoutLoading.value = false;
    window.location.reload();
  } catch (error) {
    toast.add({ severity: 'danger', summary: 'Upps!! algo ha fallado', detail: error, life: 3000 });
    loginLoading.value = false
  }
}


//iniciales avatar
const getInitials = () => {
  const fullName = user?.name+' '+user?.surnames
  const namesArray = fullName.split(' ').slice(0, 2); // Tomar solo las primeras dos palabras
  const initials = namesArray.map(name => name.charAt(0).toUpperCase()).join('');
  console.log('initials', user?.name+' '+user?.surname)
  return initials;
 
}




//collapse expand vertical menu
const isAsideOpen = ref(true)

const asideToogle = () => {
  isAsideOpen.value = !isAsideOpen.value
}

//Pan horizontal menu
const wrapper = ref(null);
const content = ref(null);

const panToRight = () => {
  wrapper.value.scrollTo(wrapper.value.scrollLeft += 300)
}

const panToLeft = () => {
  if (wrapper.value.scrollLeft > 200) {
    wrapper.value.scrollTo(wrapper.value.scrollLeft -= 300) 
  } else {
    wrapper.value.scrollTo(wrapper.value.scrollLeft = 0)  
  }
}

//get active route
const route = useRoute();
const currentRouteName = route.name;
const isLinkActive = (routeName) => {
    return route.fullPath === routeName; // Compara el to del enlace con la fullPath del objeto route
}


const adminFeatures = shallowRef([
    {
        title: 'Propiedades',
        icon: IconBuilding,
        available: true,
        color: 'indigo',
        to:'/properties'
    }, {
        title: 'Propietarios',
        icon: IconUsers,
        available: true,
        color: 'blue',
        to:'/owners'
  },
  // {
  //       title: 'Finanzas',
  //       icon: IconFinance,
  //       available: true,
  //       color: 'pink',
  //       to:'/finance'
  // },
  {
        title: 'Incidencias',
        icon: IconTool,
        available: true,
        color: 'amber',
        to:'/incidences'
    }, {
        title: 'Documentación',
        icon: IconFolders,
        available: true,
        color: 'lime',
        to:'/documents'
    }, {
        title: 'Votaciones',
        icon: IconSurvey,
        available: true,
        color: 'violet',
        to:'/surveys'
    }, {
        title: 'Comunicación',
        icon: IconSpeakerphone,
        available: true,
        color: 'teal',
         to:'/communication'
    }, {
        title: 'Reservas',
        icon: IconPin,
        available: false,
        color: 'fuchsia',
         to:'/bookings'
  },
  // {
  //       title: 'Proveedores',
  //       icon: IconWorker,
  //       available: false,
  //       color:'orange',
  //        to:'/providers'

  //   },
]);

const userFeatures = shallowRef([
    {
        title: 'Incidencias',
        icon: IconTool,
        available: true,
        color: 'amber',
        to:'/incidences'
    }, 
]);

const isAdmin = computed(() => {
  if (user?.current_community?.community_role === 'admin') {
    return true;  
  } 
    return false;  
})

const setMenu = computed(() => {
  if (isAdmin) {
       return adminFeatures.value     
  }
       return userFeatures.value
})





</script>
<style>
.smoth{
    scroll-behavior: smooth
}
/* .noScroll{
    scrollbar-gutter: stable;
} */
::-webkit-scrollbar{
    display: none;
}

</style>
