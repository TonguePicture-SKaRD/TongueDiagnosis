<!-- <template>
    <Header class="header"></Header>
    <Register_Login/>
</template>


<script setup lang="ts" name="Register">
 import { RouterLink, RouterView } from 'vue-router'
 import Header from "@/components/Header.vue";
 import Loginblock from '@/components/Loginblock.vue';
 import Register_Login from '@/components/Register_Login.vue';



</script>

<style scoped>

</style> -->

<template>
  <div :style="{ backgroundColor: backgroundColor, width: '100%', height: '100vh' }">
    <!-- 这里的 backgroundColor 是你定义的数据属性 -->
    <h1>填充页面颜色示例</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {
      backgroundColor: 'lightblue' // 设置初始背景颜色为浅蓝色
    };
  }
};
</script>

<style>
/* 在这里可以添加样式 */

</style>