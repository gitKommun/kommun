<template>
  <div class="h-full w-full flex flex-col overflow-y-scroll relative">
    <!-- breadcrum -->
    <div v-if="selectedFolder" class="flex overflow-x-scroll px-1">
      <div
        v-for="(folder, index) in path"
        :key="folder.folder_id"
        class="flex items-certer"
      >
        <template v-if="index == 0">
          <div
            @click="resetPath()"
            class="flex items-center px-2 text-xs rounded-lg hover:bg-slate-100 transition-all duration-300 cursor-pointer"
          >
            <IconFolders class="scale-75 text-slate-500" />
            <span class="ml-2 text-slate-500">Documentos</span>
          </div>
        </template>
        <template v-if="index > 0">
          <IconChevronRight class="scale-75 mx-1 text-slate-500" />
          <div
            @click="selectFolder(folder)"
            class="flex items-center px-2 text-xs rounded-lg hover:bg-slate-100 transition-all duration-300 cursor-pointer"
          >
            <IconFolder
              class="scale-75"
              :class="
                index == path.length - 1 ? 'text-indigo-500' : 'text-slate-500'
              "
            />
            <span
              class="ml-2"
              :class="
                index == path.length - 1 ? 'text-indigo-500' : 'text-slate-500'
              "
              >{{ folder.name }}</span
            >
          </div>
        </template>
      </div>
    </div>
    <!-- breadcrum -->
    <div class="w-full p-4 flex justify-between">
      <div class="flex gap-x-3">
        <InputText
          v-model="search"
          placeholder="Buscar"
          size="small"
          variant="filled"
        />
      </div>

      <AddContent
        @update:items="updateItems"
        class="h-auto"
        :selected="selectedFolder"
      />
    </div>
    <!-- content -->
    <div class="px-4">
      <div v-if="foldersLoading" class="flex items-center justify-center py-24">
        <Loading />
      </div>
      <div v-else class="flex flex-wrap gap-x-4">
        <template v-if="!folders.length">
          <div class="w-full flex flex-col items-center justify-center py-24">
            <EmptyFolder class="scale-75" />
            <span
              class="text-2xl text-center font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-500 via-sky-500 to-green-300"
            >
              Actualmente no hay documentos
            </span>
            <span class="text-sm text-slate-500 max-w-80 text-center"
              >Comienza ahora creando la estructura de documentacion de tu
              comunidad</span
            >
          </div>
        </template>
        <template v-else>
          <div class="w-full flex flex-col">
            <div
              v-if="folders.length"
              class="flex items-center justify-between py-4"
            >
              <span class="text-slate-950 font-semibold text-lg"
                >Carpetas
                <span class="text-slate-400 text-sm font-medium"
                  >({{ folders.length }})</span
                ></span
              >
            </div>
            <div
              class="w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 content-start gap-3 pb-4"
            >
              <FolderItem
                v-for="folder in folders"
                :key="folder.folder_id"
                :folder="folder"
                @update:items="updateItems"
                @click="selectFolder(folder)"
              />
              <!-- -->
            </div>
            <div
              v-if="documents.length"
              class="flex items-center justify-between py-4"
            >
              <span class="text-slate-950 font-semibold text-lg"
                >Archivos
                <span class="text-slate-400 text-sm font-medium"
                  >({{ documents.length }})</span
                ></span
              >
            </div>

            <div class="w-full" key="table">
              <DataTable
                :value="documents"
                :loading="isUpdating"
                dataKey="document_id"
                :paginator="false"
                :rows="100"
                class="text-sm"
              >
                <Column field="name" header="Documento">
                  <template #body="{ data }">
                    <span class="flex items-center">
                      <FileType :type="data.type" />
                      <span class="text-sm ml-2">{{ data.name }}</span>
                    </span>
                  </template>
                </Column>

                <Column field="upload_user" header="Propietario">
                  <template #body="{ data }">
                    <span class="flex items-center">
                      <!-- <span class="min-w-8 mr-1">
                        <Avatar label="k" shape="circle" />
                      </span> -->
                      <CustomAvatar
                        :name="data.upload_user?.Fullname || 'Kommun'"
                        class="mr-1"
                      />
                      <span class="text-xs text-slate-400 truncate">
                        {{ data.upload_user?.Fullname || "Kommun" }}
                      </span>
                    </span>
                  </template>
                </Column>

                <Column field="upload_date" header="Fecha" />

                <Column
                  :rowEditor="true"
                  style="width: 10%; min-width: 8rem"
                  bodyStyle="text-align:right"
                >
                  <template #body="{ data }">
                    <Dropdown strategy="fixed">
                      <template #reference="{ open }">
                        <div
                          class="h-8 w-8 rounded-xl hover:bg-slate-100 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer"
                          @click.stop="open"
                        >
                          <IconDotsHorizontal class="text-slate-500" />
                        </div>
                      </template>

                      <template #content="{ close }">
                        <div
                          class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm"
                        >
                          <div
                            class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
                            @click="downloadFile(data)"
                          >
                            <IconDownload class="scale-75" />
                            <span>Descargar</span>
                          </div>
                          <div
                            class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                            @click="deleteFolder(data.document_id)"
                          >
                            <IconTrash class="scale-75" />
                            <span>Eliminar</span>
                          </div>
                        </div>
                      </template>
                    </Dropdown>
                  </template>
                </Column>
              </DataTable>
            </div>
          </div>
        </template>
      </div>
    </div>
    <!-- content -->
  </div>
</template>
<script setup>
import {
  ref,
  watch,
  onMounted,
  shallowRef,
  nextTick,
  computed,
  onUnmounted,
} from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";

import AddContent from "/src/components/documents/AddContent.vue";
import FolderItem from "/src/components/documents/FolderItem.vue";
import EmptyFolder from "/src/components/emptys/EmptyFolder.vue";
import Loading from "/src/components/Loading.vue";
import Main from "/src/layouts/Main.vue";
import IconChevronRight from "@/components/icons/IconChevronRight.vue";
import IconFolder from "@/components/icons/IconFolder.vue";
import IconFolders from "@/components/icons/IconFolders.vue";
import IconTable from "@/components/icons/IconTable.vue";
import IconGrid from "@/components/icons/IconGrid.vue";
import FileType from "/src/components/FileType.vue";
import Dropdown from "/src/components/Dropdown.vue";
import IconDotsHorizontal from "/src/components/icons/IconDotsHorizontal.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";
import IconDownload from "/src/components/icons/IconDownload.vue";
import CustomAvatar from "@/components/CustomAvatar.vue";

import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

// options
defineOptions({
  name: "documents",
  layout: Main,
});

// variables
const folders = ref([]);
const documents = ref([]);
const foldersLoading = ref(true);
const selectedFolder = ref(null);
const path = ref([]);
const search = ref("");
const isUpdating = ref(false);

//utils
const http = useHttp();
const { user } = useUserStore();
const toast = useToast();

onMounted(() => {
  getFolders();
});

async function getFolders() {
  if (isUpdating.value) return;

  isUpdating.value = true;
  foldersLoading.value = true;

  try {
    const response = await http.get(
      `documents/${user?.current_community?.community_id}/folders/${
        selectedFolder?.value?.folder_id || 0
      }/`
    );

    // Actualizar los datos en un solo nextTick para evitar múltiples renders
    await nextTick(() => {
      folders.value = response.data.folders || [];
      documents.value = response.data.documents || [];
      path.value = response.data.path || [];
    });
  } catch (error) {
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  } finally {
    foldersLoading.value = false;
    isUpdating.value = false;
  }
}

function updateItems() {
  if (!isUpdating.value) {
    getFolders();
  }
}

const selectFolder = (folder) => {
  if (!isUpdating.value) {
    selectedFolder.value = folder;
    getFolders();
  }
};

const resetPath = () => {
  if (!isUpdating.value) {
    selectedFolder.value = null;
    getFolders();
  }
};

// Limpiar los datos cuando el componente se desmonta
onUnmounted(() => {
  folders.value = [];
  documents.value = [];
  path.value = [];
});

//Descarga doc
const downloadFile = async ({ document_id, name }) => {
  try {
    const response = await http.get(
      `documents/${user?.current_community?.community_id}/d/${document_id}/download/`,
      {
        responseType: "blob",
        headers: {
          Accept: "*/*",
        },
      }
    );

    const blob = new Blob([response.data], {
      type: response.headers["content-type"] || "application/octet-stream",
    });

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();

    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "El documento se ha descargado con éxito",
      life: 3000,
    });
  } catch (error) {
    console.error("Error al descargar:", error);
    toast.add({
      severity: "error",
      summary: "Upps!! algo ha fallado",
      detail: "No se pudo descargar el archivo",
      life: 3000,
    });
  }
};

// Opcional: watch para debugging
watch(
  documents,
  (newVal) => {
    console.log("Documents updated:", newVal.length);
  },
  { deep: true }
);
</script>
