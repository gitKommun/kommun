<template>
    <div class="flex flex-col items-start border p-3 rounded-2xl gap-x-3 mb-3 w-full  hover:shadow-lg  relative  transition-all duration-300"
    :class="`bg-${color()}-100 text-${color()}-600 border-${color()}-200`">
        <div class="font-bold mb-2">
            {{ zone.name }}
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
defineOptions({
    name: 'BookingZone'
})

const props = defineProps({
    zone: {
        type: Object,
    },
})
const emit = defineEmits(['update:item']);

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