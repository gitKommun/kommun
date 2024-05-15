

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vuesax from 'vuesax-alpha'
import { createPinia } from 'pinia'



import './index.css'
import 'vuesax-alpha/dist/index.css'


const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(Vuesax)
app.use(pinia)


app.mount('#app')
