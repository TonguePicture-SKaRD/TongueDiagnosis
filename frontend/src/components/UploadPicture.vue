<template>
  <el-upload
      class="upload-demo"
      drag
      multiple
      :on-change="PicOnLoad"
      :http-request="handleSuccess"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      将文件拖入此处 或 <em> 点击此处上传照片</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        舌象照片要求舌象清晰。照片上传后需等待约30s才能查询结果。<br>本测试仅做参考，不具有医学证明资格，如有不适，请去医院。
      </div>
    </template>
  </el-upload>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'
import axios from "axios";



let e;
function PicOnLoad(file){
  e = file
}

async function handleSuccess(event){
  let formData = new FormData()
  formData.append('file_data',e.raw)
  axios.post('http://127.0.0.1:5000/api/model/upload',formData,{
    headers:{
      'Content-Type':'multipart/form-data'
    }
  }).then(res=>{
    console.log(res)
  })
}
</script>

<style>

</style>