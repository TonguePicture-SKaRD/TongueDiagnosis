<script setup>
 import Header from "@/components/Header.vue";
 import Result from "@/components/Result.vue";
 import Carousel from "@/components/Carousel.vue";
 import TotalUpload from "@/components/TotalUpload.vue";
</script>

<template>
  <Header class="header"></Header>
  <Carousel class="carousel"></Carousel>
  <div class="feature"><h2><br>上传图片</h2></div>
  <TotalUpload class="upload"></TotalUpload>
  <div class="result">
    <h2><br>测试结果查看</h2>
  </div>
  <Result class="result"></Result>
</template>

<style>
body {
  background-color: #FAFAFA;
}
.header {
  position: relative;
}
.carousel {
  position: relative;
  bottom: 22px;
}
.feature ul {
  display: flex;
  position: relative;
  right: 30px;
}
.feature ul li {
  margin: auto;
  padding: 0 10px;
}
</style>