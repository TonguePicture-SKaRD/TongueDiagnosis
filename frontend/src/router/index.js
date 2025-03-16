import {createRouter, createWebHashHistory} from 'vue-router' // 使用 Hash 模式
import Home from '../views/Home.vue'
import Check from "../views/Check.vue";
import Login from "@/views/LoginRegister.vue";
import Register from "@/views/LoginRegister.vue";

const routes = [
    {
        path: '/home',
        name: 'home',
        component: Home, // 首页
        meta: {
            requireAuth: true, // 需要登录
        },
    },
    {
        path: '/login',
        name: 'login',
        component: Login, // 登录界面
    },
    {
        path: '/register',
        name: 'register',
        component: Register, // 注册界面
    },
    {
        path: '/check',
        name: 'check',
        component: Check, // 检查页面
        meta: {
            requireAuth: true, // 需要登录
        },
    },
    {
        path: '/', // 根路径重定向到首页
        redirect: '/home',
    },

];

const router = createRouter({
    history: createWebHashHistory(), // 使用 Hash 模式
    routes,
});



export default router;