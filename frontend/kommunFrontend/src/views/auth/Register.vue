
<template>
    <div class="h-screen w-screen bg-gradient-to-tr from-indigo-400 via-blue-300 to-teal-300  flex justify-center items-center">
        
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
                    <div class="flex gap-x-3">
                        <vs-input 
                            v-model="name" 
                            placeholder="Name" 
                            label-float 
                            block/>
                        <vs-input 
                            v-model="surname" 
                            placeholder="Surname" 
                            label-float 
                            block/>
                    </div>
                    <vs-input 
                        v-model="email" 
                        placeholder="E-mail"
                        type="email"
                        label-float 
                        block/>
                    <div class="flex gap-x-3">
                        <vs-input 
                            v-model="password_1" 
                            placeholder="Password" 
                            type="password"
                            label-float 
                            block/>
                        <vs-input 
                            v-model="password_2" 
                            placeholder="Password verification"
                            type="password"
                            label-float
                            block>
                            <!-- <template v-if="!passConfirm" #message-warn >no coincide</template> -->
                        </vs-input>
                    </div>
                    <div class="text-[10px] text-slate-500 px-8">
                        <span>Your password must be at least...</span>
                        <ul>
                            <li :class="[{'text-red-500':password_1!=''&&!passValidationNumber},{'text-green-500':passValidationNumber}]" type="disc">Numbers</li>
                            <li :class="[{'text-red-500':password_1!=''&&!passValidationUppercase},{'text-green-500':passValidationUppercase}]"type="disc">Capital letters</li>
                            <li :class="[{'text-red-500':password_1!=''&&!passValidationLowercase},{'text-green-500':passValidationLowercase}]"type="disc">Lowercase</li>
                            <li :class="[{'text-red-500':password_1!=''&&!passValidationDigits},{'text-green-500':passValidationDigits}]"type="disc">8 Digits</li>
                            <li :class="[{'text-red-500':password_1!=''&&!passValidationCharacter},{'text-green-500':passValidationCharacter}]"type="disc">Special characters</li>
                        </ul>
                    </div>                  
                </div>            
                <div class="flex justify-between items-center mt-4">
                    <RouterLink to="/">
                        <vs-button color="dark" type="transparent"><IconArrowBack class="mr-1 "/>Back to home</vs-button>
                    </RouterLink>
                    <vs-button color="dark" :disabled="!passConfirm">Submit</vs-button>
                </div> 
            
        </div>
    </div>
</template>
<script setup>
    import { computed, ref } from 'vue';
    import IconArrowBack from "/src/components/icons/IconArrowBack.vue"

    defineOptions({
        name: 'register',
    });
    const name = ref('');
    const surname = ref('');
    const email = ref('');
    const password_1 = ref('');
    const password_2 = ref('');

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
    const passConfirm = (() => {
        if (passFormatValid.value && password_1.value===password_2.value) {
          return true  
        }
        return false
    })

    
</script>