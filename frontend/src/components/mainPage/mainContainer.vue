<template>
  <div class="back-ground">
    <div class="common-layout">
      <Main :receivedInput="sharedInput" ref="mainRef" @get-return="handleGetReturn" @back-id="backIdToCheck"/>
      <Bottom @send-to-main="handleSendToMain" @send-picture="handleSendPicture" ref="dialogRef"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import Bottom from "./dialogBox.vue";
import Main from "./main.vue";
import {ref} from 'vue'

let sharedInput = ref('');
const mainRef = ref(null)
const dialogRef = ref(null)
const tempName = ref('')


// 处理 bottom 子组件的发送动作，将数据传递给 main 子组件
const handleSendToMain = (id: number, input: string) => {
  // console.log("main收到");
  sharedInput.value = `${id},${input}`;
  // console.log(sharedInput.value);
};

//发送图片请求
const handleSendPicture = (info) => {
  // console.log("info", info);
  initPage(info, tempName.value);
};

//初始化页面
const initPage = (basePic, sessionName) => {
  mainRef.value.initPage(basePic, sessionName);
}

//后端返回的页面信息
const inputData = (data, id) => {
  dialogRef.value.startChat()
  mainRef.value.inputData(data, id);
}

//重置页面
const resetPage = () => {
  mainRef.value.resetPage();
  dialogRef.value.backUploading();
}


//设置临时名字
const setTempName = (name) => {
  console.log(name);
  tempName.value = name;
}
defineExpose({inputData, resetPage, setTempName})

//收到回复后的操作
const handleGetReturn = (data) => {
  dialogRef.value.getReturn(data);
}

//返回id给check
const backIdToCheck = (id) => {
  emit("back-id", id);
}

const emit = defineEmits(["back-id"])
</script>

<style scoped>
.back-ground {
  height: 80vh;
  background: linear-gradient(135deg, #4facfe, rgba(90, 224, 231, 0.9), #00d4a9, #00cba9);

  background-size: 200% 200%; /* 放大背景尺寸 */

}

</style>