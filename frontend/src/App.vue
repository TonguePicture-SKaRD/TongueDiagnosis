<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
</script>
<template>
  <div class="app-container">
    <Header></Header>
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
#app {
  padding: 0;
  margin: 0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
}

.main-content {
  padding-top: 72px;
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

.main-content > * {
  min-height: calc(100vh - 72px);
}
</style>
