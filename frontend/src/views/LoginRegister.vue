<template>
  <div class="back-ground">
    <Header class="header"></Header>
    <div class="container_middle">
      <Register_Login/>
    </div>
  </div>
</template>


<script setup lang="ts">
import Header from "@/components/Header.vue";
import Register_Login from '@/components/Register_Login.vue';


</script>

<style scoped>
.container_middle {
  display: flex;
  justify-content: center;
  /* 水平居中 */
  align-items: center;
  /* 垂直居中 */
  height: 83vh;
  /* 100vh */
  width: 100%;
}

.back-ground {
  height: 100vh;
  background: linear-gradient(200deg, #f3e7e9, #cddffa);
  overflow: hidden;
}

.header {
  position: relative;
  /* background: linear-gradient(200deg, #f3e7e9, #cddffa); */
}

</style>