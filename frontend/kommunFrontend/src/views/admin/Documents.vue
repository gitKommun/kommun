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
      <InputText
        v-model="search"
        placeholder="Buscar"
        size="small"
        variant="filled"
      />
      <AddContent
        @update:items="updateItems"
        class="h-auto"
        :selected="selectedFolder"
      />
    </div>

    <div
      class="w-full flex justify-center px-4 flex-1 min-h-0 overflow-y-scroll"
    >
      <div class="w-full max-w-4xl flex flex-col">
        <div
          v-if="foldersLoading"
          class="flex items-center justify-center py-24"
        >
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
              <div class="w-full flex flex-wrap gap-3 pb-4">
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
                <SelectButton
                  v-model="toggleView"
                  :options="toggleViewOptions"
                  optionLabel="value"
                >
                  <template #option="slotProps">
                    <IconGrid v-if="slotProps.option === 'card'" />
                    <IconTable v-else />
                  </template>
                </SelectButton>
              </div>
              <transition
                enter-active-class="transition-all transition-slow ease-out overflow-hidden"
                leave-active-class="transition-all transition-slow ease-in overflow-hidden"
                enter-class="opacity-0"
                enter-to-class="opacity-100"
                leave-class="opacity-100 "
                leave-to-class="opacity-0"
                mode="out-in"
              >
                <!-- cards view -->
                <div
                  v-if="toggleView === 'card'"
                  class="w-full flex flex-wrap gap-3 pb-4"
                  key="cards"
                >
                  <DocumentItem
                    v-for="document in documents"
                    :document="document"
                    :key="document.document_id"
                    @update:items="updateItems"
                  />
                </div>
                <!-- cards view -->
                <!-- table view -->
                <div v-else class="w-full" key="table">
                  <DataTable :value="documents" class="text-sm">
                    <Column header="Documento">
                      <template #body="slotProps">
                        <span class="flex items-center">
                          <FileType :type="slotProps.data.type" />
                          <span class="text-sm ml-2">{{
                            slotProps.data.name
                          }}</span>
                        </span>
                      </template>
                    </Column>
                    <Column header="Propietario">
                      <template #body="slotProps">
                        <span class="min-w-8 mr-1">
                          <Avatar label="k" shape="circle" />
                        </span>
                        <span class="text-xs text-slate-400 truncate">{{
                          slotProps.data.upload_user
                            ? document.upload_user
                            : "Kommun"
                        }}</span>
                      </template>
                    </Column>
                    <column field="upload_date" header="Fecha" />
                    <Column
                      :rowEditor="true"
                      style="width: 10%; min-width: 8rem"
                      bodyStyle="text-align:right"
                    >
                      <template #body="slotProps">
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
                                @click="
                                  downloadFile(slotProps.data.document_id)
                                "
                              >
                                <IconDownload class="scale-75" />
                                <span>Descargar</span>
                              </div>
                              <div
                                class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                                @click="
                                  deleteFolder(slotProps.data.document_id)
                                "
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
                <!-- table view -->
              </transition>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, watch, onMounted, shallowRef } from "vue";

import AddContent from "/src/components/documents/AddContent.vue";
import FolderItem from "/src/components/documents/FolderItem.vue";
import DocumentItem from "/src/components/documents/DocumentItem.vue";
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

import { useHttp } from "/src/composables/useHttp.js";
import { useUserStore } from "/src/stores/useUserStore.js";
import { useToast } from "primevue/usetoast";

// options
defineOptions({
  name: "documents",
  layout: Main,
});

//variables
const title = ref("Documentos");
const folders = ref([]);
const foldersLoading = ref(true);
const selectedFolder = ref(null);
const documents = ref([]);
const path = ref([]);
const toggleView = ref("card");
const toggleViewOptions = ref(["card", "table"]);

//instancia API
const http = useHttp();
//user store
const { user } = useUserStore();
//use toast
const toast = useToast();

//guardar carpeta en localStorage
watch(selectedFolder, (newValue) => {
  //localStorage.setItem('currentFolder', toRaw(newValue));
});

// watch(toggleView, (newValue) => {
//   console.log('toggle', newValue)
// })

onMounted(() => {
  //selectedFolder.value = localStorage.getItem('currentFolder')
  updateItems();
});

// folders
async function getFolders() {
  //folders.value = [];
  if (selectedFolder?.value) {
    try {
      const response = await http.get(
        `documents/${user?.current_community?.community_id}/folders/${selectedFolder?.value.folder_id}`
      );

      folders.value = response.data.folders;
      path.value = response.data.path;
      documents.value = response.data.documents;

      foldersLoading.value = false;
    } catch (error) {
      toast.add({
        severity: "danger",
        summary: "Upps!! algo ha fallado",
        detail: error,
        life: 3000,
      });
    }
  } else {
    try {
      const response = await http.get(
        `documents/${user?.current_community?.community_id}/folders/0/`
      );

      folders.value = response.data.folders;
      documents.value = response.data.documents;
      path.value = response.data.path;

      foldersLoading.value = false;
    } catch (error) {
      toast.add({
        severity: "danger",
        summary: "Upps!! algo ha fallado",
        detail: error,
        life: 3000,
      });
    }
  }
}
getFolders();

function updateItems() {
  setTimeout(() => {
    getFolders();
  }, 300);
}

const selectFolder = (folder) => {
  selectedFolder.value = folder;
  updateItems();
};

const resetPath = () => {
  selectedFolder.value = null;
  updateItems();
};

//Descarga doc
const downloadFile = (id) => {
  try {
    const response = http.get(
      `documents/${user?.current_community?.community_id}/d/${id}/download/`
    );
    toast.add({
      severity: "success",
      summary: "Ok",
      detail: "El documento se ha descargado con exito",
      life: 3000,
    });
  } catch (error) {
    toast.add({
      severity: "danger",
      summary: "Upps!! algo ha fallado",
      detail: error,
      life: 3000,
    });
  }
};
</script>
