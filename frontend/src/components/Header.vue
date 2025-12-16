<script setup>
import axios from "axios";
import { ref, onMounted, watch, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const activeIndex = ref('')
const isAuthenticated = ref(false)
const userInfo = ref({
  name: 'Test User',
  avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
})
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

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
    if (res.data.code === 0) {
      isAuthenticated.value = true
      if (res.data.data) {
        userInfo.value = { ...userInfo.value, ...res.data.data }
      }
    }
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
  if (routes[key]) {
    router.push(routes[key])
    isMobileMenuOpen.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  isMobileMenuOpen.value = false
  router.push('/register')
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

onMounted(() => {
  setActiveIndex()
  fetchUserInfo()
  window.addEventListener('scroll', handleScroll)
})

watch(() => route.path, () => {
  setActiveIndex()
  isMobileMenuOpen.value = false
  fetchUserInfo()
})
</script>

<template>
  <header class="modern-header" :class="{ 'scrolled': isScrolled }">
    <div class="header-container">
      <div class="logo-section">
        <div class="logo-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L15.09 8.26L22 9L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9L8.91 8.26L12 2Z"
                  fill="currentColor"/>
          </svg>
        </div>
        <div class="logo-text">
          <span class="logo-title">TongueKit</span>
          <span class="logo-subtitle">AI Diagnosis</span>
        </div>
      </div>
      <nav class="desktop-nav">
        <div class="nav-items">
          <router-link
              to="/home"
              class="nav-item"
              :class="{ 'active': activeIndex === '2' }"
          >
            <div class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z"
                      stroke="currentColor" stroke-width="2"/>
                <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <span>Home</span>
          </router-link>
          <router-link
              to="/check"
              class="nav-item"
              :class="{ 'active': activeIndex === '3' }"
          >
            <div class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                      stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <span>Examination</span>
          </router-link>
        </div>
      </nav>
      <div class="user-section">
        <div v-if="isAuthenticated" class="user-menu">
          <el-dropdown trigger="click" popper-class="custom-dropdown">
            <div class="user-profile">
              <div class="user-avatar">
                <img :src="userInfo.avatar" :alt="userInfo.name" />
                <div class="user-status"></div>
              </div>
              <div class="user-info">
                <span class="user-name">{{ userInfo.name }}</span>
                <span class="user-role">Premium User</span>
              </div>
              <div class="dropdown-arrow">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2"/>
                </svg>
              </div>
            </div>
            <template #dropdown>
              <el-dropdown-menu class="custom-dropdown-menu">
                <el-dropdown-item class="dropdown-header">
                  <div class="user-card">
                    <img :src="userInfo.avatar" :alt="userInfo.name" class="user-card-avatar" />
                    <div class="user-card-info">
                      <div class="user-card-name">{{ userInfo.name }}</div>
                      <div class="user-card-email">{{ userInfo.email }}</div>
                    </div>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item divided class="menu-item danger" @click="logout">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9M16 17L21 12M21 12L16 7M21 12H9"
                          stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <span>Logout</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <div v-else class="auth-buttons">
          <router-link to="/register" class="auth-button">
            <span>Sign In</span>
          </router-link>
        </div>
        <button class="mobile-menu-button" @click="toggleMobileMenu">
          <svg v-if="!isMobileMenuOpen" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2"/>
          </svg>
          <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2"/>
          </svg>
        </button>
      </div>
    </div>
    <div class="mobile-menu" :class="{ 'open': isMobileMenuOpen }">
      <div class="mobile-nav">
        <router-link
            to="/home"
            class="mobile-nav-item"
            :class="{ 'active': activeIndex === '2' }"
            @click="isMobileMenuOpen = false"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z"
                  stroke="currentColor" stroke-width="2"/>
            <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>Home</span>
        </router-link>
        <router-link
            to="/check"
            class="mobile-nav-item"
            :class="{ 'active': activeIndex === '3' }"
            @click="isMobileMenuOpen = false"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                  stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>Examination</span>
        </router-link>
        <div v-if="isAuthenticated" class="mobile-user-section">
          <div class="mobile-user-profile">
            <img :src="userInfo.avatar" :alt="userInfo.name" />
            <div class="mobile-user-info">
              <span class="mobile-user-name">{{ userInfo.name }}</span>
              <span class="mobile-user-role">Premium User</span>
            </div>
          </div>
          <div class="mobile-user-actions">
            <button class="mobile-action-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z"
                      stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>Profile</span>
            </button>
            <button class="mobile-action-item" @click="logout">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9M16 17L21 12M21 12L16 7M21 12H9"
                      stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>Logout</span>
            </button>
          </div>
        </div>
        <div v-else class="mobile-auth">
          <router-link to="/register" class="mobile-auth-button" @click="isMobileMenuOpen = false">
            Sign In / Register
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.modern-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 0;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
}

.modern-header.scrolled {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(25px);
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.1);
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
}

.logo-subtitle {
  font-size: 0.75rem;
  color: #667eea;
  font-weight: 500;
  line-height: 1;
}

/* 桌面导航 */
.desktop-nav {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-items {
  display: flex;
  gap: 8px;
  background: rgba(102, 126, 234, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 12px;
  text-decoration: none;
  color: #5a6c7d;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.nav-item:hover {
  color: #667eea;
  background: rgba(255, 255, 255, 0.8);
  transform: translateY(-1px);
}

.nav-item.active {
  color: white;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.nav-icon {
  display: flex;
  align-items: center;
}

/* 用户区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  position: relative;
  width: 36px;
  height: 36px;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.user-status {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  background: #27AE60;
  border-radius: 50%;
  border: 2px solid white;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1;
}

.user-role {
  font-size: 0.75rem;
  color: #667eea;
  line-height: 1;
}

.dropdown-arrow {
  display: flex;
  align-items: center;
  color: #8b95a1;
  transition: transform 0.3s ease;
}

.user-profile:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* 认证按钮 */
.auth-button {
  padding: 10px 20px;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.auth-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* 移动端菜单按钮 */
.mobile-menu-button {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: #667eea;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-menu-button:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
}

/* 移动端菜单 */
.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(25px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transform: translateY(-100%);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.mobile-menu.open {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

.mobile-nav {
  padding: 24px;
}

.mobile-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  color: #5a6c7d;
  text-decoration: none;
  font-weight: 500;
  border-radius: 12px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.mobile-nav-item:hover,
.mobile-nav-item.active {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.mobile-user-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.mobile-user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  margin-bottom: 16px;
}

.mobile-user-profile img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.mobile-user-info {
  display: flex;
  flex-direction: column;
}

.mobile-user-name {
  font-weight: 600;
  color: #2c3e50;
}

.mobile-user-role {
  font-size: 0.8rem;
  color: #667eea;
}

.mobile-user-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mobile-action-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #5a6c7d;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.mobile-action-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.mobile-auth-button {
  display: block;
  width: 100%;
  padding: 16px;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 500;
  text-align: center;
  margin-top: 16px;
}

@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-button {
    display: flex;
  }

  .user-info {
    display: none;
  }

  .logo-text {
    display: none;
  }
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
    height: 64px;
  }

  .logo-icon {
    width: 36px;
    height: 36px;
  }

  .mobile-nav {
    padding: 20px 16px;
  }
}
</style>

<style>
.custom-dropdown {
  border-radius: 16px !important;
  border: none !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15) !important;
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(25px) !important;
  padding: 8px !important;
  margin-top: 8px !important;
}

.custom-dropdown-menu .el-dropdown-menu__item {
  border-radius: 12px !important;
  margin-bottom: 4px !important;
  padding: 0 !important;
  background: transparent !important;
  color: inherit !important;
  line-height: normal !important;
}

.custom-dropdown-menu .el-dropdown-menu__item:hover {
  background: rgba(102, 126, 234, 0.1) !important;
}

.dropdown-header {
  padding: 16px !important;
  background: transparent !important;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-card-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.user-card-info {
  display: flex;
  flex-direction: column;
}

.user-card-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.user-card-email {
  font-size: 0.875rem;
  color: #8b95a1;
}

.menu-item {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  padding: 12px 16px !important;
  color: #5a6c7d !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
}

.menu-item:hover {
  color: #667eea !important;
}

.menu-item.danger {
  color: #e74c3c !important;
}

.menu-item.danger:hover {
  color: #c0392b !important;
  background: rgba(231, 76, 60, 0.1) !important;
}
</style>
