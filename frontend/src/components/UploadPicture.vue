<template>
  <el-upload
      class="upload-demo"
      drag
      action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
      multiple
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
import {UploadFile} from "element-plus";

type UploadFiles = UploadFile[]
</script>

<style>

</style>