<template>
  <UploadPicture v-if="testState === false" :isupload="isUpload" @test="isTest"></UploadPicture>
  <Steps v-else></Steps>
  <div class="result">
    <h2><br>测试结果查看</h2>
  </div>
  <Result class="result" :isupstate="testState" @getRecord="getRecord"></Result>
</template>

<script setup>
  import { ref} from "vue";

  let isUpload = ref(0);
  import UploadPicture from "@/components/UploadPicture.vue";
  import Steps from "@/components/Steps.vue";
  import Result from "@/components/Result.vue";


  let testState = ref(false)
  const isTest = (value) =>{
    console.log("图片上传，更换图标")
    testState.value = value
  }
  const getRecord = (value) =>{
    console.log("轮询结束，恢复图标")
    testState.value = value
  }
</script>