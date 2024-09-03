<template>
    <Avatar 
        :label="getInitials()" 
        :size="size"
        shape="circle"
        :style="`background-color:${bgColor()}; color:${txtColor()}`"/>
</template>
<script setup>
defineOptions({
    name: 'CustomAvatar',
  })
    const props = defineProps({
        name: {
            type: String,
        },
        size: {
            type: String
        }
    });

    //iniciales avatar
    const getInitials = () => {
        const namesArray = props.name.split(' ').slice(0, 2); // Tomar solo las primeras dos palabras
        const initials = namesArray.map(name => name.charAt(0).toUpperCase()).join('');
        return initials;
    }
const bgColor = () => {
    const colors =  [
  '#fee2e2', // Red 100
  '#ffedd5', // Orange 100
  '#fef3c7', // Amber 100
  '#fef9c3', // Yellow 100
  '#ecfccb', // Lime 100
  '#dcfce7', // Green 100
  '#d1fae5', // Emerald 100
  '#ccfbf1', // Teal 100
  '#cffafe', // Cyan 100
  '#e0f2fe', // Sky 100
  '#dbeafe', // Blue 100
  '#e0e7ff', // Indigo 100
  '#ede9fe', // Violet 100
  '#f3e8ff', // Purple 100
  '#fae8ff', // Fuchsia 100
  '#fce7f3', // Pink 100
  '#ffe4e6', // Rose 100
];
 const colorIndex = props.name.length % colors.length;
  return colors[colorIndex];
}
const txtColor = () => {
    const colors =  [
    '#ef4444', // Red 500
    '#f97316', // Orange 500
    '#f59e0b', // Amber 500
    '#eab308', // Yellow 500
    '#84cc16', // Lime 500
    '#22c55e', // Green 500
    '#10b981', // Emerald 500
    '#14b8a6', // Teal 500
    '#06b6d4', // Cyan 500
    '#0ea5e9', // Sky 500
    '#3b82f6', // Blue 500
    '#6366f1', // Indigo 500
    '#8b5cf6', // Violet 500
    '#a855f7', // Purple 500
    '#d946ef', // Fuchsia 500
    '#ec4899', // Pink 500
    '#f43f5e', // Rose 500
    ];
 const colorIndex = props.name.length % colors.length;
  return colors[colorIndex];
}
</script>
