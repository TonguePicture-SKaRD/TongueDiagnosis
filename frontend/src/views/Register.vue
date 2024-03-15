
<template>
    <div class="common-layout">
    <el-container>
      <el-header><Header class="header"></Header></el-header>
      <el-container>
        <el-aside width="200px">Aside</el-aside>
        <el-main><Registerblock/></el-main>
      </el-container>
    </el-container>
  </div>
    <!-- <Header class="header"></Header> -->
    <h1>这是register页面</h1>
    
</template>


<script setup lang="ts" name="Register">
 import { RouterLink, RouterView } from 'vue-router'
 import Header from "@/components/Header.vue";
 import Registerblock from '@/components/Registerblock.vue';



</script>

<style scoped>

</style>