import {createRouter, createWebHashHistory} from 'vue-router' // 使用 Hash 模式
import Home from '../views/Home.vue'
import Check from "../views/Check.vue";
import Login from "@/views/LoginRegister.vue";
import Register from "@/views/LoginRegister.vue";

const routes = [
    {
        path: '/home',
        name: 'home',
        component: Home,
        meta: {
            requireAuth: true,
        },
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/register',
        name: 'register',
        component: Register,
    },
    {
        path: '/check',
        name: 'check',
        component: Check,
        meta: {
            requireAuth: true,
        },
    },
    {
        path: '/',
        redirect: '/home',
    },

];

const router = createRouter({
    history: createWebHashHistory(), // 使用 Hash 模式
    routes,
});

export default router;