<template>
  <el-carousel :interval="3000" type="card" height="200px">
    <el-carousel-item >
      <h1 text="2xl" justify="center" class="item1">使用YoLo，Unet，Resnet多种人工智能算法</h1>
    </el-carousel-item>
    <el-carousel-item >
      <h1 text="2xl" justify="center" class="item2">使用多样本训练</h1>
    </el-carousel-item>
    <el-carousel-item >
      <h1 text="2xl" justify="center" class="item3">云端计算，不耗费本地算力</h1>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.el-carousel__item h1 {
  color: #ffffff;
  opacity: 0.99;
  line-height: 200px;
  font-size: 30px;
  margin: 0;
  text-align: center;
}
.item3 {
  background-color: black;
  background-image: url("../assets/servers.png");
}
.item1 {
  background-color: black;
  background-image: url("../assets/ai.jpg");
}
.item2 {
  background-color: black;
  background-image: url("../assets/data.png");
}
</style>

<script setup>
</script>