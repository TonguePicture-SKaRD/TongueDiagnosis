<template>
  <UploadPicture v-if="testState === false" :isupload="isUpload" @test="isTest"></UploadPicture>
  <Steps v-else></Steps>
  <div class="result">
    <h2><br>测试结果查看</h2>
  </div>
  <Result class="result" :isupstate="testState" @getRecord="getRecord"></Result>
</template>

<script setup>
import {onMounted, ref} from "vue";

  let isUpload = ref(0);
  import UploadPicture from "@/components/UploadPicture.vue";
  import Steps from "@/components/Steps.vue";
  import Result from "@/components/Result.vue";
import axios from "axios";


  let testState = ref(false)
  const isTest = (value) =>{
    console.log("图片上传，更换图标")
    testState.value = value
  }
  const getRecord = (value) =>{
    console.log("轮询结束，恢复图标")
    testState.value = value
  }
function reverseArray1(arr) {
  for (let index = 0; index < Math.floor(arr.length / 2); index++) {
    // 借助第三方变量交换两个变量的值
    let temp = arr[index];
    arr[index] = arr[arr.length - 1 - index];
    arr[arr.length - 1 - index] = temp
  }
  return arr;
}
let rec = ref(0)
onMounted(function () {
  axios.get("/user/record", {
    headers:{
      'Authorization':'Bearer ' + localStorage.getItem('token')
    }
  }).then(res=> {
    console.log("拿到record，判断是否显示进度条")
    rec.value = res.data.data
    reverseArray1(rec.value)
    console.log(rec.value[0])
    if (rec.value[0].state === 0) {
      testState.value = true
    }
  }).catch(error=> {
    console.log(error);
  })
})
</script>