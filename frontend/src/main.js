import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

import axios from 'axios'
import VueAxios from 'vue-axios'

let token = localStorage.getItem('token');

axios.defaults.baseURL = 'http://127.0.0.1:5000/api';
axios.defaults.headers = {
    Authorization:"Bearer " + token
}

const app = createApp(App)
app.use(ElementPlus, { size: 'small', zIndex: 3000 })
app.use(createPinia())
app.use(router)
app.use(VueAxios, axios)
app.config.globalProperties.$axios = axios
app.mount('#app')