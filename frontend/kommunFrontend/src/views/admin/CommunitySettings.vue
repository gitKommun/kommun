<template>
  <div class="h-full w-full overflow-y-scroll">
    <div class="pl-3">
      <router-link to="/communities">
        <Button severity="contrast" text size="small">
          <IconBack class="scale-75" /> Volver a comunidades
        </Button>
      </router-link>
    </div>
    <Content>
      <GeneralData :community="community" />
      <!-- ELIMINAR COMUNIDAD -->
        <div class="w-full flex justify-between py-3">
          <div class="text-sm text-slate-400">
            Al eliminar está comunidad, tambien se eliminaran las propiedades,
            zonas comunes y usuarios vinculados con ella
          </div>
          <div class="flex-none">
            <Button @click="confirmDelete()" severity="danger"
              >Eliminar comunidad
            </Button>
          </div>
        </div>
        <ConfirmDialog></ConfirmDialog>
        <!-- ELIMINAR COMUNIDAD -->
    </Content>

  </div>
</template>
<script setup>
import { ref, onMounted, watch } from "vue";
import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";

import Main from "/src/layouts/Main.vue";
import CommonZones from "/src/components/settings/CommonZones.vue";
import GeneralData from "/src/components/settings/GeneralData.vue";
import IconBack from "/src/components/icons/IconBack.vue";
import Content from "/src/components/Content.vue";

defineOptions({
  name: "CommunitySettings",
  layout: Main,
});
//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();
const route = useRoute();
const router = useRouter();
const confirm = useConfirm();

//variables

const community_id = ref(null);
const community = ref({});
onMounted(() => {
  const { id } = route.params;
  community_id.value = id;
});

watch(community_id, (n) => {
  getCommunity();
});

const getCommunity = async () => {
  if (community_id.value) {
    try {
      const response = await http.get(`communities/${community_id.value}/`);
      community.value = response.data;
    } catch (erro) {
      toast.add({
        severity: "error",
        summary: "Upps!! algo ha fallado",
        detail: error,
        life: 3000,
      });
    }
  }
};
getCommunity();

const confirmDelete = () => {
  confirm.require({
    message:
      "Esta acción no se puede revertir, ¿ Estas seguro de borrar esta comunidad?",
    header: "Confirmación",
    rejectProps: {
      label: "Cancel",
      severity: "secondary",
      outlined: true,
    },
    acceptProps: {
      label: "Borrar",
      severity: "danger",
    },
    accept: () => {
      const response = http.delete(`communities/${community_id.value}/delete/`);
      toast.add({
        severity: "info",
        summary: "Ok",
        detail: "La comunidad se ha eliminado con exito",
        life: 3000,
      });
      router.push({ name: "communities" }).then(() => {
        window.location.reload();
      });
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Upps!!",
        detail: "No se ha podido eliminar la comunidad",
        life: 3000,
      });
    },
  });
};
</script>
