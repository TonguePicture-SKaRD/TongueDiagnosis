<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Header from "@/components/Header.vue";
import Carousel from "@/components/Carousel.vue"
import { useRouter } from "vue-router";
import TotalUpload from "@/components/TotalUpload.vue";
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'

const router = useRouter()

function jump(){
  console.log('123')
  router.push('/check')
}
</script>

<template>
  <Header class="header"></Header>
  <Carousel class="carousel"></Carousel>

  <div class="button-field">
  <span class="checkbuttonParent">
    <el-button class="checkbutton" size="large" type="primary" @click="jump">开始检测</el-button>
  </span>
  <!-- First section with instructions -->
  <span class="recordbuttonParent">
    <el-button class="recordbutton" size="large" type="success" @click="jump">检查结果</el-button>
  </span>
  </div>
  <div class="section-wrapper">
    <main>
      <section class="instruction">
        <h2>使用说明</h2>
        <p>舌象检测</p>
      </section>
    </main>
  </div>

  <!-- Rolling bar -->
  <div class="rolling-bar">
    <div class="moving-bar"></div>
  </div>




</template>

<style scoped>
header {
  background-color: #333;
  height: 500px;
  position: fixed;
  top: 0;
  left: 0;
  width: 50%;
}

.section-wrapper {
  margin-top: 50px; /* Adjust to accommodate the header */
  padding: 5px;
}

.instruction {
  text-align: center;
}

/* Rolling bar styles */
.rolling-bar {
  position: fixed;
  top: 7%; /* Place it in the middle of the viewport vertically */
  left: 0;
  width: 100%;
}

.button-field {
  display: flex;
}

.checkbuttonParent{
  position: relative;
}

.checkbutton{
  height: 400px;
  width: 400px;
}

.recordbuttonParent{
  margin-left:auto;
  position: relative;
}

.recordbutton{
  height: 400px;
  width: 400px;
}

.moving-bar {
  background-color: #ff9900;
  height: 15px;
  width: 100%;
  animation: moveBar 2s infinite alternate;
}

@keyframes moveBar {
  from { left: 0; }
  to { left: calc(100% - 100px); }
}
</style>





