<template>
    <div class="h-screen w-screen bg-emerald-200">
        <router-view></router-view>
    </div>
</template>
<script setup>
     defineOptions({
        name: 'Authenticated',
    });
</script>