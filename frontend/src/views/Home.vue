<script setup>
import Header from "@/components/Header.vue";
import {useRouter} from 'vue-router';
import Main from "@/components/mainPage/main_container.vue";
</script>

<template>
  <Header class="Header"></Header>
    <Main/>
  <!--    <Carousel class="carousel"></Carousel>-->
<!--  <section class="slider_section">-->
<!--    <div class="container">-->
<!--      <el-row>-->
<!--        &lt;!&ndash;  详细描述的区域   &ndash;&gt;-->
<!--        <el-col :span="10">-->
<!--          <div class="detail-box">-->
<!--            <h1 class="title">-->
<!--              舌诊宝： <br>-->
<!--              中医AI智能舌诊系统-->
<!--            </h1>-->
<!--            <p>-->
<!--              本作品的创意来源为使用深度学习创造新的应用模式，对中医学科当中的舌象识别方面有重要应用价值，同时有助于推进中医与机器学习等高新科技的结合。-->
<!--            </p>-->
<!--            <router-link to="/check">-->
<!--              进行检测-->
<!--            </router-link>-->
<!--          </div>-->
<!--        </el-col>-->
<!--        <el-col :span="6"></el-col>-->
<!--        <el-col :span="8">-->
<!--          <el-card class="card">-->
<!--            <h1 class="cardTitle">舌象上传与诊断</h1>-->
<!--            <p>-->
<!--              平台具有初步舌象诊断功能，实现了舌象的上传、诊断并且生成健康报告和建议。<br>-->
<!--              您可以通过自己的设备进行舌象的上传，平台将会对上传的舌象进行诊断并生成健康报告。-->
<!--            </p>-->
<!--          </el-card>-->
<!--          <el-card class="card">-->
<!--            <h1 class="cardTitle">诊断记录查看</h1>-->
<!--            <p>-->
<!--              诊断记录查看为您提供了健康报告的查询服务，包括健康报告记录列表显示，以及对应记录查询。<br>-->
<!--              健康报告将按照时间进行降序排序，方便您查询到自己最近的健康诊断报告。-->
<!--            </p>-->
<!--          </el-card>-->
<!--        </el-col>-->
<!--      </el-row>-->
<!--    </div>-->
<!--  </section>-->


</template>


<style scoped>
.Header {
  height: 60px;
}


</style>