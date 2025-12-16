<script setup>
import axios from "axios";
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const activeIndex = ref('')
const isAuthenticated = ref(false)

const setActiveIndex = () => {
  activeIndex.value = route.path === '/check' ? '3' : '2'
}

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
    isAuthenticated.value = res.data.code === 0
  } catch (error) {
    console.error('authentication failure:', error)
    localStorage.removeItem('token')
    await router.push('/register')
  }
}

const handleSelect = (key) => {
  const routes = {
    1: '/home',
    2: '/home',
    3: '/check'
  }
  if (routes[key]) router.push(routes[key])
}

const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  router.push('/register')
}

onMounted(() => {
  setActiveIndex()
  fetchUserInfo()
})

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
    <div style="display: flex">
      <el-menu-item index="1" disabled>
        <span class="logo_word">Tongue Diagnosis Kit</span>
      </el-menu-item>
      <el-menu-item index="2"><h3>Home</h3></el-menu-item>
      <el-menu-item index="3"><h3>Examination</h3></el-menu-item>
    </div>

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
          <span style="margin-left: 8px">Test User</span>
        </template>
        <el-menu-item index="5-1" @click="logout">Logout</el-menu-item>
      </el-sub-menu>
      <el-menu-item v-else index="5" class="right-align">
        <router-link to="/register" style="color: inherit; text-decoration: none">
          Log in / Register
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