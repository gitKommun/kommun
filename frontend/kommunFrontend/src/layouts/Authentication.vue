<template>
    <div class="h-screen w-screen bg-gradient-to-tr from-indigo-400 via-blue-300 to-teal-300 ">
        <slot />
    </div>
</template>
<script setup>
     defineOptions({
        name: 'Authentication',
    });
</script>