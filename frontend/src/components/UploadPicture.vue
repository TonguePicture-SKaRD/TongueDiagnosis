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
      将文件拖入此处 或 <em> 点击此处上传照片</em>
    </div>
  </el-upload>
</template>

<script setup lang="ts">
import {UploadFilled} from '@element-plus/icons-vue'
import axios from "axios";
import {ElMessage} from 'element-plus'

const emit = defineEmits(["success"])

let e; // 这个是上传图片的文件
let base64String = ""; // 存储 Base64 编码的字符串

// 提取 Base64 编码
function PicOnLoad(file) {
  e = file;
  const reader = new FileReader();

  reader.onload = function (event) {
    base64String = event.target?.result as string;
    // console.log("Base64 编码：", base64String);
  };

  reader.readAsDataURL(file.raw); // 读取文件并转换为 Base64
}

async function handleSuccess(event) {
  if (!e || !e.raw) {
    console.error("未找到要上传的文件");
    return;
  }

  //
  // let formData = new FormData();
  // formData.append('file_data', e.raw);


  setTimeout(() => {
    // console.log("上传的文件：", base64String);
    console.log("上传的文件：", e.raw);
    emit("success", {success: true, base64: base64String, fileData: e.raw});
  }, 600);
  // emit("success", {success: true, base64: base64String});

  // axios.post('/model/upload', formData, {
  //   headers: {
  //     'Content-Type': 'multipart/form-data',
  //     'Authorization': 'Bearer ' + localStorage.getItem('token')
  //   },
  //   timeout: 30000 // ⏳ 设置超时时间 30 秒
  // }).then(res => {
  //   console.log("图像上传成功");
  //
  //   // 触发事件，传递上传成功状态和 Base64 数据
  //   emit("success", {success: true, base64: base64String});
  //
  //   ElMessage({
  //     showClose: true,
  //     message: '上传成功，请等待约30秒',
  //     type: 'success',
  //   });
  // }).catch(error => {
  //   if (error.code === 'ECONNABORTED') {
  //     console.log('上传超时');
  //     ElMessage({
  //       showClose: true,
  //       message: '上传超时，请检查网络并重试',
  //       type: 'error',
  //     });
  //   } else {
  //     console.log(error);
  //     ElMessage({
  //       showClose: true,
  //       message: '图片上传失败，请确认网络环境',
  //       type: 'error',
  //     });
  //   }
  // });
}
</script>

<style scoped>
/* 调整上传组件的整体大小 */
.upload-demo {
  width: 400px; /* 设定宽度 */
  height: 180px; /* 设定高度 */
}

/* 修改拖拽框的背景色、边框、颜色 */
:deep(.el-upload-dragger) {
  background-color: #f0f9ff; /* 背景颜色 */
  border: 2px dashed #409eff; /* 边框样式 */
  border-radius: 8px; /* 圆角 */
  color: #333; /* 文字颜色 */
  height: 100%; /* 让高度撑满父容器 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 修改上传图标的颜色 */
:deep(.el-icon--upload) {
  font-size: 50px; /* 调整图标大小 */
  color: #409eff; /* 图标颜色 */
}

/* 修改“将文件拖入此处”文字样式 */
:deep(.el-upload__text) {
  font-size: 16px;
  font-weight: bold;
  color: #606266;
}
</style>
