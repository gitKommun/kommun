<template>
    <div class="h-full w-full  pt-16 ">
        <h1 class="text-6xl font-extrabold text-slate-700 mb-4">Hola {{email}}</h1>
        <Cover/>
        <Features :email="email"/>
        <Pricing/>
        <vs-button color="dark" type="border" @click="logout" class="mt-8 w-full">Cerrar sesión</vs-button>
    </div>   
</template>
<script setup >
import Guests from '/src/layouts/Guests.vue';
import Features from '/src/views/landing-modules/Features.vue';
import Cover from '/src/views/landing-modules/Cover.vue';
import Pricing from '/src/views/landing-modules/Pricing.vue';

import axios from 'axios';
import { ref } from 'vue';


function listCookieNames() {
    const cookies = document.cookie;  // Obtener el string completo de cookies
    if (!cookies) {
        console.log('No cookies found');  // No hay cookies disponibles
        return;
    }
}

// Configura axios para manejar las cookies y los headers CSRF
axios.defaults.withCredentials = true;  // Asegúrate de que las cookies se envíen con cada solicitud
axios.defaults.withXSRFToken = true;
//axios.defaults.xsrfCookieName = 'csrftoken';  // Nombre de la cookie CSRF
//axios.defaults.xsrfHeaderName = 'X-CSRFToken';  // Nombre del header CSRF


axios.interceptors.request.use(config => {
    listCookieNames();
    const csrfToken = getCSRFToken();
    console.log('Attempting to set CSRF Token:', csrfToken); // Intenta establecer el token CSRF

    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
        console.log('CSRF Token set in headers:', config.headers['X-CSRFToken']); // Muestra el token CSRF que se establece en las cabeceras
    }

    return config;
}, error => {
    console.error('Error configuring request:', error); // Muestra errores en la configuración de la solicitud
    return Promise.reject(error);
});

const email = ref('');

function getCSRFToken() {
    const name = 'csrftoken=';
    let decodedCookie = decodeURIComponent(document.cookie);
    console.log('Decoded cookies:', decodedCookie); // Muestra todas las cookies decodificadas

    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            let token = c.substring(name.length, c.length);
            console.log('CSRF Token found:', token); // Muestra el token CSRF encontrado
            return token;
        }
    }
    console.log('No CSRF Token found'); // Informa si no se encuentra el token
    return "";
}

// Ejemplo de solicitud GET
axios.get('https://burly-agreement-production.up.railway.app/members/user_email/', {
    withCredentials: true
})
.then(response => {
    email.value = response.data.email;
    console.group('Request');
    console.log('sessionid:', document.cookie.split('; ').find(row => row.startsWith('sessionid=')));
    console.groupEnd();
})
.catch(error => {
    console.group('Request');
    console.log('sessionid:', document.cookie.split('; ').find(row => row.startsWith('sessionid=')));
    console.groupEnd();
    console.group('Response');
    console.log('status:', error.response.status);
    console.log('headers:', error.response.headers);
    console.log('data:', error.response.data);
    console.groupEnd();
});

// Función para cerrar sesión
const logout = () => {
    axios.post('https://burly-agreement-production.up.railway.app/members/logout/', {}, {
        withCredentials: true,
        withXSRFToken: true,
        //headers: {
        //    'X-XSRF-TOKEN': getCsrfToken()
        //}    
    })
}

defineOptions({
    name: 'Landing',
    layout: Guests,
});
</script>

