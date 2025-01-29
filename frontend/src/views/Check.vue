<script setup>
import Header from "@/components/Header.vue";
import {useRouter} from 'vue-router';
import Main from "@/components/mainPage/mainContainer.vue";
</script>

<template>
  <div class="back-ground">
    <Header class="Header"></Header>
    <Main/>
  </div>
</template>


<style scoped>
.Header {
  height: 60px;
}

.back-ground {
  background: linear-gradient(200deg, #f3e7e9, #cddffa);
  height: 100vh;
  overflow: hidden;

}
</style>