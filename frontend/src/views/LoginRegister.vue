<template>
  <div class="back-ground">
<!--    <Header class="header"></Header>-->
    <div class="container_middle">
      <Register_Login/>
    </div>
  </div>
</template>

<script setup>
import Header from "@/components/Header.vue";
import Register_Login from '@/components/Register_Login.vue';
</script>

<style scoped>
.container_middle {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 83vh;
  width: 100%;
}

.back-ground {
  height: 100vh;
  background: linear-gradient(200deg, #f3e7e9, #cddffa);
  overflow: hidden;
}

.header {
  position: relative;
}
</style>