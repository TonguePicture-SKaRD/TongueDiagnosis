<!--<script lang="ts" setup>-->
<!--import {ref} from 'vue';-->
<!--import {useRouter} from 'vue-router';-->
<!--import router from '@/router'-->

<!--import {getCurrentInstance, onBeforeMount} from "vue";-->
<!--import axios from "axios";-->

<!--// let {proxy} = getCurrentInstance();-->

<!--// 检测当前页面并且正确显示黄线-->
<!--let a;-->
<!--const routers = useRouter()-->
<!--console.log('router:', routers.currentRoute.value.path);-->
<!--if (routers.currentRoute.value.path == "/home") a = '2';-->
<!--if (routers.currentRoute.value.path == "/check") a = '3';-->
<!--const activeIndex = ref(a)-->
<!--const handleSelect = (key: number, keyPath: string[]) => {-->
<!--  // console.log(key, keyPath)-->
<!--  if (key == 1) router.push('./home');-->
<!--  if (key == 2) router.push('./home');-->
<!--  if (key == 3) router.push('./check');-->
<!--}-->

<!--const isl = ref(1);-->
<!--let token = localStorage.getItem('token');-->
<!--onBeforeMount(() => {-->
<!--  //调用方法-->
<!--  axios.get("/user/info", {-->
<!--        headers: {-->
<!--          "Authorization": "Bearer " + token-->
<!--        }-->
<!--      })-->
<!--      .then(function (res) {-->
<!--        // console.log(res.data.code)-->
<!--        isl.value = res.data.code;-->
<!--        // console.log(isl.value);-->
<!--      })-->
<!--      .catch(function (error) {-->
<!--        // console.log(error);-->
<!--        router.push('/register')-->
<!--      });-->
<!--});-->

<!--function logout() {-->
<!--  window.localStorage.removeItem('token')-->
<!--  // console.log("登出成功")-->
<!--  window.location.reload()-->
<!--  // console.log("刷新成功")-->
<!--}-->
<!--</script>-->

<!--<template>-->
<!--  <el-menu-->
<!--      :default-active="activeIndex"-->
<!--      class="el-menu-demo"-->
<!--      mode="horizontal"-->
<!--      background-color="#545c64"-->
<!--      text-color="#fff"-->
<!--      active-text-color="#ffd04b"-->
<!--      @select="handleSelect"-->
<!--      style="display: flex; justify-content: space-between;"-->
<!--  >-->
<!--    &lt;!&ndash; 左侧部分包裹容器 &ndash;&gt;-->
<!--    <div style="display: flex;">-->
<!--      <el-menu-item index="1" disabled>-->
<!--        <span class="logo_word">舌 诊 宝</span>-->
<!--      </el-menu-item>-->
<!--      <el-menu-item index="2"><h3>首页</h3></el-menu-item>-->
<!--      <el-menu-item index="3"><h3>检测</h3></el-menu-item>-->
<!--    </div>-->

<!--    &lt;!&ndash; 右侧部分 &ndash;&gt;-->
<!--    <div>-->
<!--      <el-sub-menu index="5" v-if="isl" class="right-align">-->
<!--        <template #title>-->
<!--          <el-avatar :size="40" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"/>-->
<!--          <span style="margin-left: 8px">用户 User</span>-->
<!--        </template>-->
<!--        <el-menu-item index="5-1" @click="logout">登出</el-menu-item>-->
<!--      </el-sub-menu>-->
<!--      <el-menu-item v-else index="5" class="right-align">-->
<!--        <router-link to="/register">登录/注册</router-link>-->
<!--      </el-menu-item>-->
<!--    </div>-->
<!--  </el-menu>-->
<!--</template>-->

<!--<style>-->
<!--.el-menu-item.is-disabled {-->
<!--  color: white !important;-->
<!--  opacity: 1 !important;-->
<!--}-->

<!--.logo_word {-->
<!--  font-size: 20px;-->
<!--  font-weight: bold;-->
<!--}-->

<!--/* 右侧对齐样式 */-->
<!--.right-align {-->
<!--  margin-left: auto !important;-->
<!--}-->
<!--</style>-->



<script setup>
import axios from "axios";
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 响应式状态
const activeIndex = ref('')
const isAuthenticated = ref(false)

// 根据路由设置激活菜单项
const setActiveIndex = () => {
  activeIndex.value = route.path === '/check' ? '3' : '2'
}

// 获取用户信息
const fetchUserInfo = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    await router.push('/register')
    return
  }

  try {
    const res = await axios.get('/user/info', {
      headers: { Authorization: `Bearer ${token}` }
    })
    // 根据实际接口返回判断登录状态
    isAuthenticated.value = res.data.code === 0
  } catch (error) {
    console.error('认证失败:', error)
    localStorage.removeItem('token')
    await router.push('/register')
  }
}

// 处理菜单选择
const handleSelect = (key) => {
  const routes = {
    1: '/home',
    2: '/home',
    3: '/check'
  }
  if (routes[key]) router.push(routes[key])
}

// 登出功能
const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  router.push('/register')
}

// 生命周期
onMounted(() => {
  setActiveIndex()
  fetchUserInfo()
})

// 监听路由变化
watch(() => route.path, () => {
  setActiveIndex()
})
</script>

<template>
  <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      class="el-menu-demo"
      @select="handleSelect"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      style="display: flex; justify-content: space-between;"
  >
    <!-- 左侧菜单 -->
    <div style="display: flex">
      <el-menu-item index="1" disabled>
        <span class="logo_word">舌 诊 宝</span>
      </el-menu-item>
      <el-menu-item index="2"><h3>首页</h3></el-menu-item>
      <el-menu-item index="3"><h3>检测</h3></el-menu-item>
    </div>

    <!-- 右侧用户区域 -->
    <div>
      <el-sub-menu
          index="5"
          v-if="isAuthenticated"
          class="right-align"
      >
        <template #title>
          <el-avatar
              :size="40"
              src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
          />
          <span style="margin-left: 8px">用户 User</span>
        </template>
        <el-menu-item index="5-1" @click="logout">登出</el-menu-item>
      </el-sub-menu>
      <el-menu-item v-else index="5" class="right-align">
        <router-link to="/register" style="color: inherit; text-decoration: none">
          登录/注册
        </router-link>
      </el-menu-item>
    </div>
  </el-menu>
</template>

<style>
.el-menu-item.is-disabled {
  color: white !important;
  opacity: 1 !important;
}

.logo_word {
  font-size: 20px;
  font-weight: bold;
}

.right-align {
  margin-left: auto !important;
}
</style>