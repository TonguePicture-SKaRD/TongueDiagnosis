import './assets/main.css'
import {createApp} from 'vue'
import {createPinia} from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'

let token = localStorage.getItem('token');

axios.defaults.baseURL = 'http://localhost:5000/api';
axios.defaults.headers = {
    Authorization: "Bearer " + token
}

const app = createApp(App)
app.use(ElementPlus, {size: 'small', zIndex: 3000})
app.use(createPinia())
app.use(router)
app.use(VueAxios, axios)
app.config.globalProperties.$axios = axios
app.mount('#app')

router.beforeEach((to, from, next) => {
    // Using the route guard, if the user is not logged in, they will be redirected to the login page.
    if (to.matched.some((auth) => auth.meta.requireAuth)) {
        let token = localStorage.getItem("token");
        if (token) {
            next();
        } else {
            next({
                path: '/register'
            });
        }
    } else {
        next();
    }
})
