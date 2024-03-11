<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// 检测当前页面并且正确显示黄线
var a;
const router = useRouter()
console.log('router:',router.currentRoute.value.path);
if (router.currentRoute.value.path == "/home") a = '2';
if (router.currentRoute.value.path == "/check") a = '3';

const activeIndex = ref(a)
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>


<template>
<!--顶栏组件-->
  <div class="Header" />
  <!--element+的menu组件-->
  <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      @select="handleSelect"
  >
    <!--logo-->
    <el-menu-item index="1"><h1><router-link to="/home">舌诊宝</router-link></h1></el-menu-item>
    <!--导航栏-->
    <el-menu-item index="2"><h3><router-link to="/home">首页</router-link></h3></el-menu-item>
    <el-menu-item index="3"><h3><router-link to="/check">检测</router-link></h3></el-menu-item>
    <el-menu-item index="4"><h3><router-link to="/home">其他</router-link></h3></el-menu-item>
  </el-menu>
  <!--用户logo(伪)-->
  <div class="user">
    <ul>
      <li><h2><a href="#" class="logo">头像</a></h2></li>
      <li><h2><a href="#">用户user</a></h2></li>
    </ul>
  </div>
</template>


<style>
/*用户头像*/
.user {
  display:flex;
  width: 150px;
  margin: 0 auto;
  position: relative;
  bottom: 52px;
  left: 500px;
}
.user ul {
  margin: auto;
  display: flex;
}
.user ul li {
  display: flex;
  margin: auto;
  list-style: none;
}
.user ul li a {
  margin: auto;
  text-decoration: none;
  font-size: 16px;
  color: #ffffff;
}
.user ul li a.logo {
  display: block;
  width: 30px;
  height: 30px;
  border-radius: 100%;
  background-image: url("../assets/Chat_Tongue.jpg");
  font-size: 0px;
}
</style>