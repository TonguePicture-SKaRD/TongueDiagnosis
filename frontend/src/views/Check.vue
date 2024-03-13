<script setup>
 import Header from "@/components/Header.vue";
 import Upload from "@/components/UploadPicture.vue"
 import Result from "@/components/Result.vue";
 import Carousel from "@/components/Carousel.vue";
</script>

<template>
  <Header class="header"></Header>
  <Carousel class="carousel"></Carousel>
  <div class="feature"><h2><br>上传图片</h2></div>
  <Upload class="upload"></Upload>
  <div class="result">
    <h2><br>测试结果查看</h2>
  </div>
  <Result class="result"></Result>
</template>

<style>
body {
  background-color: #fffef6;
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