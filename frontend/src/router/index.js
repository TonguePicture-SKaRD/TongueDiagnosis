import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Check from "../views/Check.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView //首页
    },
    {
      path: '/login',
      name: 'login',
      component: Login //登录界面
    },
    {
      path: '/register',
      name: 'register',
      component: Register //登录界面
    },
    {
      path: '/check',
      name: 'check',
      component: Check
    },
    {
      path:'',
      redirect:'/home' // 重定向，即最初路径为根路径时，立即重定向到/home路径
    }
  ],
})

export default router


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
        path: "/register"
      });
    }
  } else {
    next();
  }
})