<template>
    <div class="relative w-screen h-screen overflow-hidden">
        <img src="@/assets/bg.jpg"  class="absolute top-0 left-0 w-full h-full object-cover ">
        <div class="h-screen w-screen relative z-10">
             <slot />
        </div>
    </div>
    
</template>
<script setup>
     defineOptions({
        name: 'Authentication',
    });
</script>