<script setup>
import Register_Login from '@/components/Register_Login.vue';
</script>

<template>
  <div class="back-ground">
    <div class="container_middle">
      <Register_Login/>
    </div>
  </div>
</template>

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