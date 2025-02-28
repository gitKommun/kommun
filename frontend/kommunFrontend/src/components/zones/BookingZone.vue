<template>
    <div class="flex flex-col items-start border p-3 rounded-2xl gap-x-3 mb-3 w-full  hover:shadow-lg  relative  transition-all duration-300"
    :class="`bg-${color()}-100 text-${color()}-600 border-${color()}-200`">
        <div class="w-full flex item-center justify-between font-bold mb-2">
            <span class="truncate">{{ zone.name }}</span>
            <Dropdown strategy="fixed">
                  <template #reference="{ open }">
                    <div
                      class="h-8 w-8 rounded-xl bg-white/40 hover:bg-white/80 justify-center items-center flex flex-none transition-all duration-300 cursor-pointer"
                      @click="open"
                    >
                      <IconDots :class="`text-${color()}-600`" />
                    </div>
                  </template>
                  <template #content="{ close }">
                    <div
                      class="w-40 rounded-2xl bg-white p-3 shadow-2xl gap-y-2 text-sm"
                    >
                      <div
                        class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer"
                        @click="updateZone()"
                      >
                        <IconPencil class="scale-75 text-slate-900" />
                        <span class=" text-slate-900">Editar</span>
                      </div>
                      <div
                        class="flex items-center gap-x-2 p-2 rounded-lg hover:bg-slate-50 transition-all duration-300 cursor-pointer text-red-500"
                        @click="deleteZone()"
                      >
                        <IconTrash class="scale-75" />
                        <span>Eliminar</span>
                      </div>
                    </div>
                  </template>
                </Dropdown>
        </div>
        <div class="flex flex-col items-start gap-x-2 py-1">
            <span class="text-xs uppercase ">Tiempo de reserva</span>
            <span>{{ zone.reservation_duration }} {{ zone.time_unit }}</span>
        </div>
        <div class="w-full py-2 mt-2">
            <Button severity="contrast" size="small" class="w-full" label="reservar"  @click="toBook()"/>
        </div>
    </div>
</template>
<script setup>
import IconDots from "/src/components/icons/IconDots.vue";
import IconPencil from "/src/components/icons/IconPencil.vue";
import IconTrash from "/src/components/icons/IconTrash.vue";
import Dropdown from "/src/components/Dropdown.vue";
defineOptions({
    name: 'BookingZone'
})

const props = defineProps({
    zone: {
        type: Object,
    },
})
const emit = defineEmits(['update:item', 'update:edit', 'update:delete']);

//updateZone
const updateZone = () => {
    emit('update:edit', true);
}

//deleteZone
const deleteZone = () => {
    emit('update:delete', true);
}

const toBook = () => {
    emit('update:item', true);
}


const color = () => {
    const colors =  [
  'red', // Red 100
  'orange', // Orange 100
  'amber', // Amber 100
  'yellow', // Yellow 100
  'lime', // Lime 100
  'green', // Green 100
  'emerald', // Emerald 100
  'teal', // Teal 100
  'cyan', // Cyan 100
  'sky', // Sky 100
  'blue', // Blue 100
  'indigo', // Indigo 100
  'violet', // Violet 100
  'purple', // Purple 100
  'fuchsia', // Fuchsia 100
  'pink', // Pink 100
  'rose', // Rose 100
];
 const colorIndex = props.zone.name.length % colors.length;
  return colors[colorIndex];
}


</script>