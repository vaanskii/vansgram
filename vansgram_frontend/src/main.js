import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_URL

const app = createApp(App)

app.use(createPinia())
app.use(router, axios)

app.mount('#app')
