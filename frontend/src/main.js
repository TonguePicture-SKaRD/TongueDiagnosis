import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'

import App from './App.vue'
import router from './router'

import axios from 'axios'
import VueAxios from 'vue-axios'

axios.defaults.baseURL = 'http://127.0.0.1:5000/api';
axios.defaults.headers = {
    Authorization:"Bearer "+"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJRCI6NiwiZW1haWwiOiIxMjM0NTZAcXEuY29tIiwiZXhwIjoxNzEwNTc0MjA4fQ.NaWgmzeKejzARM9pZAl1xHxk4OGsaZROq7bXtkrusR4"
}

const app = createApp(App)
app.use(ElementPlus, { size: 'small', zIndex: 3000 })
app.use(createPinia())
app.use(router)
app.use(VueAxios, axios)
app.config.globalProperties.$axios = axios
app.mount('#app')