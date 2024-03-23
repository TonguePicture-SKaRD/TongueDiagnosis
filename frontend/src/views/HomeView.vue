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

  <div class="checkbutton">
    <el-button type="primary" @click="jump">开始检测</el-button>
  </div>
  <!-- First section with instructions -->
  <div class="recordbutton">
    <el-button type="success" @click="jump">查看结果</el-button>
  </div>>
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
.header {
  background-color: #333;
  height: 500px;
  position: fixed;
  top: 0;
  left: 0;
  width: 50%;
}

.section-wrapper {
  margin-top: 300px; /* Adjust to accommodate the header */
  padding: 20px;
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





