import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Check from "../views/Check.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: Home,//首页
      meta: {
        requireAuth: true,  // 判断是否需要登录
      },
    },
    {
      path: '/login',
      name: 'login',
      component: Login//登录界面
    },
    {
      path: '/register',
      name: 'register',
      component: Register //登录界面
    },
    {
      path: '/check',
      name: 'check',
      component: Check,
      meta: {
        requireAuth: true,  // 判断是否需要登录
      },
    },
    {
      path:'',
      redirect:'/home' // 重定向，即最初路径为根路径时，立即重定向到/home路径
    }
  ],
})

export default router


