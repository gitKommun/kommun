
<template>
    <div class="h-screen w-screen  flex justify-center items-center">
        
        <div class="flex flex-col bg-white  rounded-2xl shadow-2xl overflow-hidden p-4">
  
                <div class="flex items-center">
                    <div class="flex justify-center">
                        <img alt="Kommun logo" class="h-24 -ml-2" src="@/assets/iso_kommun.svg"  />
                    </div>
                    <div class="">
                        <h1 class="text-3xl font-bold px-4">Empecemos!!</h1>
                        <p class="text-slate-500 text-sm px-4"> Bienvennido a kommun, es hora de construir una comunidad</p>
                    </div>
                </div>
                <div class="flex flex-col gap-y-2 px-2">
                    <div class="flex gap-x-3 py-4">
                        <InputText 
                            v-model="name" 
                            placeholder="Name" 
                            class="w-full"
                            variant="filled"/>
                        <InputText
                            v-model="surnames" 
                            placeholder="Surname" 
                            class="w-full"
                            variant="filled"/>
                    </div>
                    <div class="py-4">
                        <InputText 
                            v-model="email" 
                            placeholder="E-mail"
                            type="email"
                            class="w-full"
                            variant="filled"/>
                    </div> 
                    <div class="flex gap-x-3 py-4">
                        <div class="w-full">
                            <Password
                            v-model="password_1" 
                            placeholder="Contraseña" 
                            inputClass="min-w-full"
                            toggleMask
                            variant="filled"
                            promptLabel="Elige contraseña" weakLabel="Muy debil" mediumLabel="Debil" strongLabel="Segura"
                            :fluid="true">
                            <template #footer>
                                <ul class="text-xs mt-2 pl-2">
                                    <li :class="[{'text-red-500':password_1!=''&&!passValidationNumber},{'text-green-500':passValidationNumber}]" type="disc">Numbers</li>
                                    <li :class="[{'text-red-500':password_1!=''&&!passValidationUppercase},{'text-green-500':passValidationUppercase}]"type="disc">Capital letters</li>
                                    <li :class="[{'text-red-500':password_1!=''&&!passValidationLowercase},{'text-green-500':passValidationLowercase}]"type="disc">Lowercase</li>
                                    <li :class="[{'text-red-500':password_1!=''&&!passValidationDigits},{'text-green-500':passValidationDigits}]"type="disc">8 Digits</li>
                                    <li :class="[{'text-red-500':password_1!=''&&!passValidationCharacter},{'text-green-500':passValidationCharacter}]"type="disc">Special characters</li>
                                </ul>
                            </template>
                        </Password>
                        </div>
                        <div class="w-full">
                            <Password
                            v-model="password_2" 
                            placeholder="Confirmar contraseña"
                            inputClass="w-full"
                            :feedback="false"
                            toggleMask
                            variant="filled"
                            fluid/>
                        </div>
                        
                        
                    </div>
                 
                                   
                </div>            
                <div class="flex justify-between items-center mt-4">
                    <RouterLink to="/">
                        <Button size="small" text><IconArrowBack class="mr-1 "/>Back to home</Button>
                    </RouterLink>
                    <Button  @click="registerUser" :loading="registerLoading" label="crear" severity="contrast" class="min-w-32" raised/>
                </div> 
            
        </div>
    </div>
</template>
<script setup>
import { computed, ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import IconArrowBack from "/src/components/icons/IconArrowBack.vue"
import Authentication from '/src/layouts/Authentication.vue';
import { useRouter } from 'vue-router';
//Jakub: enlazando con API
import { useHttp } from '/src/composables/useHttp.js'; 

//utils
const http = useHttp();
const router = useRouter();
const toast = useToast();


   defineOptions({
        name: 'register',
        layout:Authentication
    });
    const name = ref('');
    const surnames = ref('');
    const email = ref('');
    const password_1 = ref('');
    const password_2 = ref('');

//login
 const login = () => {
    try {
        const response =  http.post(`members/login/`, {
            email: email.value,
            password: password.value,
        });
        
        const { csrftoken, sessionid } = response.data;

        setCookie('csrftoken', csrftoken, 30);
        setCookie('sessionid', sessionid, 30);

        router.push({ name: 'onboarding' });
    } catch (error) {

        // Manejar el error de autenticación
        toast.add({
            severity: 'danger',
            summary: 'Upps!! algo ha fallado',
            detail: error,
            life: 3000
        });

    }
}
//register
const registerLoading = ref(false);
const registerUser = () => {
    registerLoading.value = true
    try {
        if (passFormatValid.value) {
            if (password_1.value===password_2.value) {
                const response = http.post(`members/register/`, {
                    name: name.value,
                    surnames: surnames.value,
                    email: email.value,
                    password: password_1.value
                    // Agrega aquí los demás campos del formulario que desees enviar
                    });
                
                
            } else {
                toast.add({
                    severity: 'danger',
                    summary: 'Las contraseñas no coinciden',
                    detail: 'Comprueba que has introducido la misma contraseña en los dos campos',
                    life: 3000
                });
            }
        } else {
            toast.add({
                severity: 'danger',
                summary: 'Formato de contraseña no valido',
                detail: 'Revisa los requisitos para tener una contraseña segura',
                life: 3000
            });
        }
        registerLoading.value = false

    } catch (error) {
        toast.add({ severity: 'danger', summary: 'Error en el registro', detail: error, life: 3000 });
        registerLoading.value = false
    }
    login()

};
//Jakub: fin

 

    const passValidationNumber = computed(() => {
        if (/\d/.test(password_1.value)) {
            return true
        }
        return false
    })
    const passValidationUppercase = computed(() => {
        if (/(.*[A-Z].*)/.test(password_1.value)) {
            return true
        }
        return false
    })
    const passValidationLowercase = computed(() => {
        if (/(.*[a-z].*)/.test(password_1.value))  {
            return true
        }
        return false
    })
    const passValidationDigits = computed(() => {
        if (password_1.value.length >= 8) {
            return true
        }
        return false
    })
    const passValidationCharacter = computed(() => {
        if (/[^A-Za-z0-9]/.test(password_1.value)) {
            return true
        }
        return false
    })
    const passFormatValid = computed(() => {
        if (passValidationCharacter.value && passValidationDigits.value && passValidationLowercase.value && passValidationUppercase.value && passValidationNumber.value) {
            return true
        }
        return false
    })
    const passConfirm = computed (() => {
        if (passFormatValid.value && password_1.value===password_2.value) {
          return true  
        }
        return false
    })

   

    
</script>