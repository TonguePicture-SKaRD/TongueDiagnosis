<script lang="ts" setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import router from '@/router'

import {getCurrentInstance, onBeforeMount} from "vue";

let {proxy} = getCurrentInstance();

// 检测当前页面并且正确显示黄线
let a;
const routers = useRouter()
console.log('router:', routers.currentRoute.value.path);
if (routers.currentRoute.value.path == "/home") a = '2';
if (routers.currentRoute.value.path == "/check") a = '3';
const activeIndex = ref(a)
const handleSelect = (key: number, keyPath: string[]) => {
  // console.log(key, keyPath)
  if (key == 1) router.push('./home');
  if (key == 2) router.push('./home');
  if (key == 3) router.push('./check');
  if (key == 4) router.push('./home');
}

const isl = ref(1);
let token = localStorage.getItem('token');
// onBeforeMount(() => {
//   //调用方法
//   proxy.$http
//       .get("/user/info", {
//         headers: {
//           "Authorization": "Bearer " + token
//         }
//       })
//       .then(function (res) {
//         // console.log(res.data.code)
//         isl.value = res.data.code;
//         // console.log(isl.value);
//       })
//       .catch(function (error) {
//         // console.log(error);
//         router.push('/register')
//       });
// });

function logout() {
  window.localStorage.removeItem('token')
  // console.log("登出成功")
  window.location.reload()
  // console.log("刷新成功")
}
</script>

<template>
  <!--顶栏组件-->
  <div class="Header">
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
      <el-menu-item index="1"><h1>舌诊宝</h1></el-menu-item>
      <!--导航栏-->
      <el-menu-item index="2"><h3>首页</h3></el-menu-item>
      <el-menu-item index="3"><h3>检测</h3></el-menu-item>
      <el-menu-item index="4"><h3>其他</h3></el-menu-item>
    </el-menu>
    <!--用户logo,条件渲染-->
    <div class="user" v-if="isl == 0">
      <!--    <ul>-->
      <!--      <li><h2><a href="#" class="logo">头像</a></h2></li>-->
      <!--      <li><h2><a href="#">用户user</a></h2></li>-->
      <!--    </ul>-->

      <el-dropdown>
    <span class="el-dropdown-link">
      <ul>
      <li><h2><a href="#" class="logo">头像</a></h2></li>
      <li><h2><a href="#">用户user</a></h2></li>
    </ul>
    </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">登出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
    <div class="nouser" v-else>
      <ul>
        <li>
          <h3>
            <router-link to="/register">登录</router-link>
          </h3>
        </li>
        <li>
          <h3>
            <router-link to="/register">注册</router-link>
          </h3>
        </li>
      </ul>
    </div>
  </div>
</template>


<style>

/*用户头像*/
.user {
  display: flex;
  width: 150px;
  margin: 0 auto;
  position: relative;
  bottom: 48px;
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

.nouser {
  display: flex;
  width: 150px;
  margin: 0 auto;
  position: relative;
  bottom: 46px;
  left: 500px;
}

.nouser ul {
  margin: auto;
  display: flex;
}

.nouser ul li {
  display: flex;
  margin: auto;
  list-style: none;
}

.nouser ul li a {
  margin: auto;
  text-decoration: none;
  font-size: 16px;
  color: #ffffff;
}
</style>