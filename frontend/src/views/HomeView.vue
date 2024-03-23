<script setup>
 import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <h1>这是home页面</h1>
  <router-link to='/check'>到check页面</router-link>
  <div>
    <header>
      <div class="moving-bar"></div>
    </header>
    <main>
      <section class="instruction">
        <h2>使用说明</h2>
        <p>舌象检测</p>
      </section>
    </main>
  </div>
  <div>
    <header>
      <div class="moving-bar">
        <div class="block"></div>
        <div class="block"></div>
        <div class="block"></div>
      </div>
    </header>
    <main>
      <section class="instruction">
        <h2>Instructions</h2>
        <p>Write your instructions here...</p>
      </section>
    </main>
  </div>

</template>

<script>
export default {
  name: 'Homepage',
  // Add any script logic here if needed
};

</script>

<style scoped>
header {
  background-color: #333;
  height: 50px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
}

.moving-bar {
  background-color: #ff9900; /* Adjust color as needed */
  height: 5px;
  width: 100%;
  animation: moveBar 2s infinite alternate;
}

@keyframes moveBar {
  from { left: 0; }
  to { left: calc(100% - 100px); } /* Adjust as needed */
}

main {
  margin-top: 60px; /* Adjust to accommodate the header */
  padding: 20px;
}

.instruction {
  text-align: center;
}

/* Additional styles as needed */
header {
  background-color: #333;
  height: 50px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
}

.moving-bar {
  background-color: #ff9900; /* Adjust color as needed */
  height: 5px;
  width: 100%;
  animation: moveBar 2s infinite alternate;
}

@keyframes moveBar {
  from { left: 0; }
  to { left: calc(100% - 100px); } /* Adjust as needed */
}

main {
  margin-top: 60px; /* Adjust to accommodate the header */
  padding: 20px;
}

.instruction {
  text-align: center;
}

/* Additional styles as needed */

</style>




