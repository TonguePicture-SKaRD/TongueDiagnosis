<template>
  <div class="back-ground">
    <div class="common-layout">
      <Main :receivedInput="sharedInput" ref="mainRef"/>
      <Bottom @send-to-main="handleSendToMain" @send-picture="handleSendPicture"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import Bottom from "./dialogBox.vue";
import Main from "./main.vue";
import {ref} from 'vue'

let sharedInput = ref('');
const mainRef = ref(null)

// 处理 bottom 子组件的发送动作，将数据传递给 main 子组件
const handleSendToMain = (id: number, input: string) => {
  // console.log("main收到");
  sharedInput.value = `${id},${input}`;
  // console.log(sharedInput.value);
};

//发送图片且有结果后
const handleSendPicture = (info) => {
  initPage(info.base64, info.ans);
};

//初始化页面
const initPage = (basePic, ans) => {
  mainRef.value.initPage(basePic, ans);
}
</script>

<style scoped>
.back-ground {
  height: 80vh;
  background: linear-gradient(135deg, #4facfe, rgba(90, 224, 231, 0.9), #00d4a9, #00cba9);

  background-size: 200% 200%; /* 放大背景尺寸 */

}

</style>