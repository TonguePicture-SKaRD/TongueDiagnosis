<script setup lang="ts">
import {UploadFilled} from '@element-plus/icons-vue'
import axios from "axios";
import {ElMessage} from 'element-plus'

const emit = defineEmits(["success"])

let e;
let base64String = "";

function PicOnLoad(file) {
  e = file;
  const reader = new FileReader();
  reader.onload = function (event) {
    base64String = event.target?.result as string;
  };
  reader.readAsDataURL(file.raw);
}

async function handleSuccess(event) {
  if (!e || !e.raw) {
    console.error("未找到要上传的文件");
    return;
  }

  setTimeout(() => {
    console.log("上传的文件：", e.raw);
    emit("success", {success: true, base64: base64String, fileData: e.raw});
  }, 600);
}
</script>

<template>
  <el-upload
      class="upload-demo"
      drag
      multiple
      :on-change="PicOnLoad"
      :http-request="handleSuccess"
      accept=".jpg,.jpeg,.png,.bmp"
      :show-file-list="false"
  >
    <el-icon class="el-icon--upload">
      <upload-filled/>
    </el-icon>
    <div class="el-upload__text">
      Drag the file here or<em> Click here to upload a photo </em>
    </div>
  </el-upload>
</template>

<style scoped>
.upload-demo {
  width: 400px;
  height: 180px;
}

:deep(.el-upload-dragger) {
  background-color: #f0f9ff;
  border: 2px dashed #409eff;
  border-radius: 8px;
  color: #333;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

:deep(.el-icon--upload) {
  font-size: 50px;
  color: #409eff;
}

:deep(.el-upload__text) {
  font-size: 16px;
  font-weight: bold;
  color: #606266;
}
</style>
