<template>
    <div class="h-full w-full">
        <header class="bg-white text-gray-600">
            <div class="container mx-auto flex items-center justify-between py-2 px-6">
                <RouterLink to="/">
                    <img alt="Kommun logo" class="h-12" src="@/assets/logo_kommun.svg"  />
                </RouterLink>
                <div class="hidden md:flex items-center space-x-4">
                    <RouterLink to="/">features</RouterLink>
                    <RouterLink to="/">About us</RouterLink>
                </div>
                <div class="flex items-center space-x-4">
                    <button class="bg-transparent text-gray-100 py-2 px-4 border border-gray-100 hover:border-transparent rounded transition duration-200">Login</button>
                    <button class="bg-gray-700 text-white py-2 px-4 rounded hover:bg-gray-600 transition duration-200">Registro</button>
                </div>
                <div class="md:hidden flex items-center">
                    <button id="menu-toggle" class="text-gray-200 focus:outline-none">
                    <i class="fas fa-bars"></i>
                    </button>
                </div>
            </div>
        </header>
        <RouterView />
    </div>
</template>
<script setup></script>