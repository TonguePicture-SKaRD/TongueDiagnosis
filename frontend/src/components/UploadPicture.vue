<template>
  <el-upload
      class="upload-demo"
      drag
      multiple
      :on-change="PicOnLoad"
      :http-request="handleSuccess"
      accept=".jpg,.jpeg,.png,.bmp"
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
import {defineEmits} from 'vue'
import axios from "axios";
import {ref} from "vue";
import { ElMessage } from 'element-plus'
// const props = defineProps(['isupload'])
const emit = defineEmits(["test"])

let e;//这个是上传图片的文件
function PicOnLoad(file){
  e = file
}
async function handleSuccess(event){
  let formData = new FormData()
  formData.append('file_data',e.raw)
  axios.post('/model/upload',formData,{
    headers:{
      'Content-Type':'multipart/form-data',
      'Authorization':'Bearer ' + localStorage.getItem('token')
    }
  }).then(res=>{
    console.log("图像上传成功")
    emit("test",true)
    // props.isupload = 1
    ElMessage({
      showClose: true,
      message: '上传成功，请等待约30秒',
      type: 'success',
    })
  }).catch(error => {
    console.log(error)
    ElMessage({
      showClose: true,
      message: '图片上传失败，请确认网络环境',
      type: 'error',
    })
  })
}
</script>

<style>

</style>