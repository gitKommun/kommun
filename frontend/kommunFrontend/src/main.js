

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
//import Vuesax from 'vuesax3'
import Vuesax from 'vuesax-alpha'

import './index.css'
//import 'vuesax3/dist/vuesax.css'

import 'vuesax-alpha/dist/index.css'
// vuesax darkmode
import 'vuesax-alpha/theme-chalk/dark/css-vars.css'

const app = createApp(App)

app.use(router)
app.use(Vuesax)

app.mount('#app')
