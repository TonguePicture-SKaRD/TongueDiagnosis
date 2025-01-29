<script setup>
import Header from "@/components/Header.vue";
import { useRouter } from 'vue-router';

</script>

<template>
  <Header class="header"></Header>
  <!--    <Carousel class="carousel"></Carousel>-->
  <section class="slider_section">
    <div class="container">
      <el-row>
        <!--  详细描述的区域   -->
        <el-col :span="10">
          <div class="detail-box">
            <h1 class="title">
              舌诊宝： <br>
              中医AI智能舌诊系统
            </h1>
            <p>
              本作品的创意来源为使用深度学习创造新的应用模式，对中医学科当中的舌象识别方面有重要应用价值，同时有助于推进中医与机器学习等高新科技的结合。
            </p >
            <router-link to="/check">
              进行检测
            </router-link >
          </div>
        </el-col>
        <el-col :span="6"></el-col>
        <el-col :span="8">
          <el-card class="card">
            <h1 class="cardTitle">舌象上传与诊断</h1>
            <p>
              平台具有初步舌象诊断功能，实现了舌象的上传、诊断并且生成健康报告和建议。<br>
              您可以通过自己的设备进行舌象的上传，平台将会对上传的舌象进行诊断并生成健康报告。
            </p>
          </el-card>
          <el-card class="card">
            <h1 class="cardTitle">诊断记录查看</h1>
            <p>
              诊断记录查看为您提供了健康报告的查询服务，包括健康报告记录列表显示，以及对应记录查询。<br>
              健康报告将按照时间进行降序排序，方便您查询到自己最近的健康诊断报告。
            </p>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </section>
</template>


<style scoped>
.Header{
  height: 60px;
}


.title {
  color: black;
  font-size: 50px;
  font-weight: bolder;
}

.slider_section {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  background-image: url("../assets/home_back .jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  height: 950px;
  width: auto;
}

.container {
  margin-left: 5%;
  margin-right: 5%;
  margin-top: 10%;
  width: 100%;
}

.slider_section .row {
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

.slider_section #customCarousel1 {
  width: 100%;
  position: unset;
}

.slider_section .detail-box {
  padding-bottom: 90px;
  width: 100%;
}

.slider_section .detail-box p {
  color: #444;
  font-size: 15px;
}

.slider_section .detail-box a {
  display: inline-block;
  font-family: 'Merriweather Sans', sans-serif;
  text-transform: uppercase;
  padding: 10px 45px;
  background-color: darkgoldenrod;
  border: 1px solid #ff8a1d;
  border-radius: 5px;
  color: white;
  margin-top: 15px;
}

.slider_section .detail-box a:hover {
  background-color: transparent;
  color: darkgoldenrod;
}

.slider_section .img-box img {
  width: 100%;
}

.card {
  max-width: 480px;
  background-color: white;
  opacity: 0.5;
  margin-top: 10%;
}

.cardTitle {
  color: black;
  font-weight: bolder;
}


</style>