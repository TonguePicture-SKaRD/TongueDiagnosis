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
  email: 'user@example.com'
})
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)
const headerKey = ref(0)

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
      // 假设返回用户信息
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
  headerKey.value++
})
</script>

<template>
  <header class="modern-header" :class="{ 'scrolled': isScrolled }" :key="headerKey">
    <div class="header-container">
      <!-- Logo区域 -->
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

      <!-- 桌面导航 -->
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

      <!-- 用户区域 -->
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

                <el-dropdown-item divided class="menu-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z"
                          stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <span>Profile Settings</span>
                </el-dropdown-item>

                <el-dropdown-item class="menu-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M16 4H18C18.5304 4 19.0391 4.21071 19.4142 4.58579C19.7893 4.96086 20 5.46957 20 6V18C20 18.5304 19.7893 19.0391 19.4142 19.4142C19.0391 19.7893 18.5304 20 18 20H16M12 15L16 11M16 11L12 7M16 11H4"
                          stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <span>View Reports</span>
                </el-dropdown-item>

                <el-dropdown-item class="menu-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                          stroke="currentColor" stroke-width="2"/>
                    <path d="M19.4 15C19.2669 15.3016 19.2272 15.6362 19.286 15.9606C19.3448 16.285 19.4995 16.5843 19.73 16.82L19.79 16.88C19.976 17.0657 20.1235 17.2863 20.2241 17.5291C20.3248 17.7719 20.3766 18.0322 20.3766 18.295C20.3766 18.5578 20.3248 18.8181 20.2241 19.0609C20.1235 19.3037 19.976 19.5243 19.79 19.71C19.6043 19.896 19.3837 20.0435 19.1409 20.1441C18.8981 20.2448 18.6378 20.2966 18.375 20.2966C18.1122 20.2966 17.8519 20.2448 17.6091 20.1441C17.3663 20.0435 17.1457 19.896 16.96 19.71L16.9 19.65C16.6643 19.4195 16.365 19.2648 16.0406 19.206C15.7162 19.1472 15.3816 19.1869 15.08 19.32C14.7842 19.4468 14.532 19.6572 14.3543 19.9255C14.1766 20.1938 14.0813 20.5082 14.08 20.83V21C14.08 21.5304 13.8693 22.0391 13.4942 22.4142C13.1191 22.7893 12.6104 23 12.08 23C11.5496 23 11.0409 22.7893 10.6658 22.4142C10.2907 22.0391 10.08 21.5304 10.08 21V20.91C10.0723 20.579 9.96512 20.2579 9.77251 19.9887C9.5799 19.7194 9.31074 19.5143 9 19.4C8.69838 19.2669 8.36381 19.2272 8.03941 19.286C7.71502 19.3448 7.41568 19.4995 7.18 19.73L7.12 19.79C6.93425 19.976 6.71368 20.1235 6.47088 20.2241C6.22808 20.3248 5.96783 20.3766 5.705 20.3766C5.44217 20.3766 5.18192 20.3248 4.93912 20.2241C4.69632 20.1235 4.47575 19.976 4.29 19.79C4.10405 19.6043 3.95653 19.3837 3.85588 19.1409C3.75523 18.8981 3.70343 18.6378 3.70343 18.375C3.70343 18.1122 3.75523 17.8519 3.85588 17.6091C3.95653 17.3663 4.10405 17.1457 4.29 16.96L4.35 16.9C4.58054 16.6643 4.73519 16.365 4.794 16.0406C4.85282 15.7162 4.81312 15.3816 4.68 15.08C4.55324 14.7842 4.34276 14.532 4.07447 14.3543C3.80618 14.1766 3.49179 14.0813 3.17 14.08H3C2.46957 14.08 1.96086 13.8693 1.58579 13.4942C1.21071 13.1191 1 12.6104 1 12.08C1 11.5496 1.21071 11.0409 1.58579 10.6658C1.96086 10.2907 2.46957 10.08 3 10.08H3.09C3.42099 10.0723 3.742 9.96512 4.01127 9.77251C4.28053 9.5799 4.48572 9.31074 4.6 9C4.73312 8.69838 4.77282 8.36381 4.714 8.03941C4.65519 7.71502 4.50054 7.41568 4.27 7.18L4.21 7.12C4.02405 6.93425 3.87653 6.71368 3.77588 6.47088C3.67523 6.22808 3.62343 5.96783 3.62343 5.705C3.62343 5.44217 3.67523 5.18192 3.77588 4.93912C3.87653 4.69632 4.02405 4.47575 4.21 4.29C4.39575 4.10405 4.61632 3.95653 4.85912 3.85588C5.10192 3.75523 5.36217 3.70343 5.625 3.70343C5.88783 3.70343 6.14808 3.75523 6.39088 3.85588C6.63368 3.95653 6.85425 4.10405 7.04 4.29L7.1 4.35C7.33568 4.58054 7.63502 4.73519 7.95941 4.794C8.28381 4.85282 8.61838 4.81312 8.92 4.68H9C9.29577 4.55324 9.54802 4.34276 9.72569 4.07447C9.90337 3.80618 9.99872 3.49179 10 3.17V3C10 2.46957 10.2107 1.96086 10.5858 1.58579C10.9609 1.21071 11.4696 1 12 1C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V3.09C14.0013 3.41179 14.0966 3.72618 14.2743 3.99447C14.452 4.26276 14.7042 4.47324 15 4.6C15.3016 4.73312 15.6362 4.77282 15.9606 4.714C16.285 4.65519 16.5843 4.50054 16.82 4.27L16.88 4.21C17.0657 4.02405 17.2863 3.87653 17.5291 3.77588C17.7719 3.67523 18.0322 3.62343 18.295 3.62343C18.5578 3.62343 18.8181 3.67523 19.0609 3.77588C19.3037 3.87653 19.5243 4.02405 19.71 4.21C19.896 4.39575 20.0435 4.61632 20.1441 4.85912C20.2448 5.10192 20.2966 5.36217 20.2966 5.625C20.2966 5.88783 20.2448 6.14808 20.1441 6.39088C20.0435 6.63368 19.896 6.85425 19.71 7.04L19.65 7.1C19.4195 7.33568 19.2648 7.63502 19.206 7.95941C19.1472 8.28381 19.1869 8.61838 19.32 8.92V9C19.4468 9.29577 19.6572 9.54802 19.9255 9.72569C20.1938 9.90337 20.5082 9.99872 20.83 10H21C21.5304 10 22.0391 10.2107 22.4142 10.5858C22.7893 10.9609 23 11.4696 23 12C23 12.5304 22.7893 13.0391 22.4142 13.4142C22.0391 13.7893 21.5304 14 21 14H20.91C20.5882 14.0013 20.2738 14.0966 20.0055 14.2743C19.7372 14.452 19.5268 14.7042 19.4 15Z"
                          stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <span>Settings</span>
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

        <!-- 移动端菜单按钮 -->
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

    <!-- 移动端菜单 -->
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

/* Logo区域 */
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
  background: linear-gradient(45d, #667eea 0%, #764ba2 100%);
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
