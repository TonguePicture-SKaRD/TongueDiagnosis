<template>
  <div
      class="draggable-container"
      :style="{ top: `${position.y}px`, left: `${position.x}px`, position: 'absolute', transition: 'top 0.s ease, left 0.s ease' }"
      ref="draggableContainer"
  >

    <!--         上传图片组件-->
    <div v-if="sendPic" class="upload-wrapper">
      <el-icon class="arrow-left">
        <ArrowRightBold/>
      </el-icon>

      <div v-if="isUploading">
        <Steps ref="stepRef"/>
      </div>
      <div v-else>
        <UploadPicture @success="startQuest" style="margin-top: 5px"/>
      </div>


      <el-icon class="arrow-right">
        <ArrowLeftBold/>
      </el-icon>
    </div>


    <div class="drag-handle" @mousedown="startDrag" v-if="!sendPic">
      <el-icon>
        <Rank/>
      </el-icon>
    </div>

    <input @keydown="handleKeyDown" class="message-input" v-model="inputValue" placeholder="请在此输入"
           style="height: auto;" v-if="!sendPic">
    <el-button type="success" :icon="Promotion" @click="sendToMain" size="large" style="font-size: 20px;" circle
               v-if="!sendPic"/>
    <!-- 点击按钮控制语音识别的开始和停止 -->
    <el-button
        :type="isRecording ? 'warning' : 'primary'"
        :icon="isRecording ? CircleClose:Microphone"
        @click="toggleVoiceRecognition"
        size="large"
        :loading="isLoading"
        style="font-size: 20px;"
        circle
        v-if="!sendPic"
    />


  </div>
</template>

<script setup lang="ts">
import {ref, reactive, onBeforeMount, computed, nextTick} from 'vue'
import {Promotion, Rank, Microphone, CircleClose, ArrowLeftBold, ArrowRightBold} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import {useStateStore} from '@/stores/stateStore';
// 获取 Pinia Store
const stateStore = useStateStore();
import UploadPicture from '@/components/UploadPicture.vue'; // 导入上传图片组件
import Steps from "@/components/Steps.vue";
import axios from "axios"; //导入上传模组
let sendPic = ref(true); // 记录现在是否要发送图片
let isUploading = ref(false);//是否正在发送
const stepRef = ref(null) //动态加载的变化

// 定义 emit 函数
const emit = defineEmits(['send-to-main', 'send-picture']);

// 输入框的本地数据
let inputValue = ref('');

// 发送输入内容给父组件
let ask_tip = 0;
const sendToMain = () => {
  // console.log(`发送${inputValue.value}到main`);
  emit('send-to-main', ask_tip, inputValue.value);
  ask_tip += 1;
  inputValue.value = '';
};

// 语音输入的逻辑
// 状态管理
const isRecording = ref(false);
const isLoading = ref(false);
const result = ref("");

//初始化url
let baseURL = '';
onBeforeMount(() => {
  if (stateStore.baseUrl == "0") {
    ErrorPop("Please set an url", 5000)
  }
  baseURL = stateStore.baseUrl;


});
let recognition = null;

//舌头的分类
const tongueDictionary = {
  color: [
    "舌色：淡白舌,",
    "舌色：淡红舌,",
    "舌色：红舌,",
    "舌色：绛舌,",
    "舌色：青紫舌,"
  ],
  outcolor: [
    "舌苔颜色：白苔,",
    "舌苔颜色：黄苔,",
    "舌苔颜色：灰黑苔,"
  ],
  rot: [
    "舌苔腻,",
    "舌苔腐,"
  ],
  thick: [
    "舌头薄,",
    "舌头厚,"
  ]
};


//获取查看记录
async function getRecordData() {
  try {
    const response = await axios.get('/user/record', {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      }
    });
    return response.data
  } catch (error) {
    console.error('获取 /user/record 失败:', error);
    return null; // 失败时返回 null
  }
}

// 切换语音识别状态
const toggleVoiceRecognition = () => {
  if (isRecording.value) {
    // 如果正在监听，停止识别
    stopRecognition();
  } else {
    // 如果未在监听，启动识别
    startRecognition();
  }
};

//重新开始加载
const resetLoading = () => {
  stepRef.value.resetCountdown()
}


// 初始化语音识别
if ('webkitSpeechRecognition' in window) {
  recognition = new webkitSpeechRecognition();
  recognition.continuous = false; // 设为非连续模式
  recognition.interimResults = false; // 只返回最终结果
  recognition.lang = 'zh-CN'; // 设定语言为中文

  recognition.onstart = () => {
    isRecording.value = true;

  };

  recognition.onresult = (event) => {
    inputValue.value += event.results[0][0].transcript;
  };

  recognition.onerror = (event) => {
    ErrorPop('语音识别出错，请重试');
  };

  recognition.onend = () => {
    isRecording.value = false;
  };
} else {
  console.warn('当前浏览器不支持语音识别');
}

// 开始语音识别
const startRecognition = () => {

  if (recognition) {
    recognition.start();
    console.log("开始语音识别")
  } else {
    ErrorPop('您的浏览器不支持语音识别');
  }
};

// 停止语音识别
const stopRecognition = () => {
  if (recognition) {
    console.log("停止语音识别")
    recognition.stop();
  }
};


//选择音频类型
let audioType = ref("De");


// 拖动框的逻辑
interface Position {
  x: number;
  y: number;
}

interface Offset {
  x: number;
  y: number;
}

const position = reactive<Position>({x: window.innerWidth - 850, y: window.innerHeight - 250}) // 初始位置
const offset = reactive<Offset>({x: 0, y: 0})
let isDragging = ref<boolean>(false)
const draggableContainer = ref<HTMLDivElement | null>(null)

// 拖动相关函数
const startDrag = (event: MouseEvent): void => {
  if (draggableContainer.value) {
    const rect = draggableContainer.value.getBoundingClientRect()
    isDragging.value = true
    offset.x = event.clientX - rect.left
    offset.y = event.clientY - rect.top
    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', endDrag)
  }
}

const onDrag = (event: MouseEvent): void => {
  if (isDragging.value) {
    // 限制拖动范围
    position.x = Math.max(0, Math.min(event.clientX - offset.x, window.innerWidth - (draggableContainer.value?.offsetWidth || 0)));
    position.y = Math.max(0, Math.min(event.clientY - offset.y, window.innerHeight - (draggableContainer.value?.offsetHeight || 0)));
  }
};

const endDrag = (): void => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
}

// 按下 Enter 键触发发送消息
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    sendToMain();
  }
};

//错误弹窗
const ErrorPop = (info: string, time = 3000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'error',
    duration: time
  })
}

//图片的码
let pic64 = ref("")
//开始查询
const startQuest = async (info) => {
  if (info.success) {
    pic64.value = info.base64
  }
  console.log("开始");
  emit("send-picture", {base64: pic64.value,fileData: info.fileData})
  startLoading();
  // pollGetRecord();
}

//轮询
async function pollGetRecord(interval = 2000, startTime = Date.now()) {
  try {
    const responseData = await getRecordData();
    const data = responseData.data;

    if (data && data[data.length - 1].state === 1) {
      const endTime = Date.now(); // 记录结束时间
      const elapsedTime = (endTime - startTime) / 1000; // 计算总耗时（秒）

      console.log("✅ 获取到符合条件的数据:", data[data.length - 1].result);
      console.log(`🎯 轮询耗时: ${elapsedTime.toFixed(2)} 秒`);
      const result = data[data.length - 1].result
      let ans = ''

      ans += tongueDictionary.color[result.tongue_color]
      ans += tongueDictionary.outcolor[result.coating_color]
      ans += tongueDictionary.thick[result.tongue_thickness]
      ans += tongueDictionary.rot[result.rot_greasy]
      console.log(ans)
      emit("send-picture", {base64: pic64.value, ans: ans})
      startChat();


      return data[data.length - 1].result; // 返回数据并停止轮询
    }

    console.log("🔄 数据不符合条件，继续轮询...");
    setTimeout(() => pollGetRecord(interval, startTime), interval); // 递归调用继续轮询
  } catch (error) {
    console.error("❌ 轮询获取数据失败:", error);
    setTimeout(() => pollGetRecord(interval, startTime), interval); // 发生错误时继续轮询
  }
}

//恢复上传界面
const backUploading = () => {
  sendPic.value = true
  isUploading.value = false
}

//开始加载
const startLoading = async () => {
  isUploading.value = true
  await nextTick()
  resetLoading();
}

const startChat = () => {
  sendPic.value = false
  isUploading.value = false
}

//得到回复
const getReturn = (data) => {
  if (data.success) startChat()
  else backUploading()
}
defineExpose({startChat, startLoading, backUploading, getReturn})
</script>


<style scoped>
.draggable-container {
  display: flex;
  align-items: center;
  width: 550px;
  background-color: #f5f5f5;
  border-radius: 30px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #ddd;
  cursor: move;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  justify-content: center; /* 水平居中 */
}

.draggable-container:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.drag-handle {
  margin-right: 10px;
  cursor: grab;
}

.drag-handle img {
  width: 24px;
  height: 24px;
}

.message-input {
  flex: 1;
  border: none;
  padding: 10px;
  outline: none;
  border-radius: 20px;
  font-size: 16px;
  font-family: 'Roboto', sans-serif; /* 添加好看的字体 */
  line-height: 1.5; /* 增加行高，使得文本看起来更整齐 */
  background-color: transparent;
}


.send-button svg {
  fill: #000;
}


.upload-wrapper {
  display: flex;
  align-items: center;
  gap: 20px; /* 控制左右箭头和 UploadPicture 之间的间距 */
}

.arrow-left, .arrow-right {
  font-size: 24px;
  color: #409eff; /* 调整箭头颜色 */
  cursor: pointer;
}

.arrow-left:hover, .arrow-right:hover {
  color: #66b1ff; /* 悬停时颜色变深 */
}

.input-container {
  display: flex; /* 让子元素横向排列 */
  align-items: center; /* 让子元素垂直居中 */
  gap: 10px; /* 子元素之间的间距 */
}

</style>