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
//
router.beforeEach((to, from, next) => {
    /**
     * 未登录则跳转到登录页
     * 未登录跳转到登录页,也可以通过axios的响应拦截器去实现,但是会先在当前页面渲染一下,再跳转到登录页,会有个闪动的现象
     * 这里通过路由守卫的方式,不会在当前页闪现一下,但是需要在每个路由组件添加一个是否需要登录的标识位,如本项目中的requireAuth字段
     */
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