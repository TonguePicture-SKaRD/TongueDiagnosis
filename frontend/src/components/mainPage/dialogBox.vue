<template>
  <div
      class="draggable-container"
      :style="{ top: `${position.y}px`, left: `${position.x}px`, position: 'absolute', transition: 'top 0.s ease, left 0.s ease' }"
      ref="draggableContainer"
  >
    <div class="drag-handle" @mousedown="startDrag">
      <el-icon>
        <Rank/>
      </el-icon>
    </div>
    <input @keydown="handleKeyDown" class="message-input" v-model="inputValue" placeholder="Please enter here"
           style="height: auto;">
    <el-button type="success" :icon="Promotion" @click="sendToMain" size="large" style="font-size: 20px;" circle/>
    <!-- 点击按钮控制语音识别的开始和停止 -->
    <el-button
        :type="isRecording ? 'warning' : 'primary'"
        :icon="isRecording ? CircleClose:Microphone"
        @click="toggleVoiceRecognition"
        size="large"
        :loading="isLoading"
        style="font-size: 20px;"
        circle
    ></el-button>
    <!--    选择语音类型-->

    <!-- 按钮 -->
    <!-- 按钮 -->
    <el-dropdown trigger="click" @command="handleCommand">
      <el-button type="info" size="large" class="dropdown-button" circle>
        {{ audioType }}
      </el-button>
      <template #dropdown>
        <el-dropdown-item command="De">Default</el-dropdown-item>
        <el-dropdown-item command="L">Lei</el-dropdown-item>
        <el-dropdown-item command="Di">Ding</el-dropdown-item>
        <el-dropdown-item command="C">Cai</el-dropdown-item>
        <el-dropdown-item command="S">Sun</el-dropdown-item>
        <el-dropdown-item command="P">Pang</el-dropdown-item>
        <el-dropdown-item command="B">Bei</el-dropdown-item>
        <el-dropdown-item command="N">Nai</el-dropdown-item>
      </template>
    </el-dropdown>


  </div>
</template>

<script setup lang="ts">
import {ref, reactive, onBeforeMount} from 'vue'
import {Promotion, Rank, Microphone, CircleClose} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import {useStateStore} from '@/stores/stateStore';
// 获取 Pinia Store
const stateStore = useStateStore();

// 定义 emit 函数
const emit = defineEmits(['send-to-main']);

// 输入框的本地数据
let inputValue = ref('');

// 发送输入内容给父组件
let ask_tip = 0;
const sendToMain = () => {
  // console.log(`发送${inputValue.value}到main`);
  emit('send-to-main', [ask_tip, inputValue.value]);
  ask_tip += 1;
  inputValue.value = '';
};

// 语音输入的逻辑
// 状态管理
const isRecording = ref(false);
const isLoading = ref(false);
const result = ref("");

// 用于存储录音的数据
let mediaRecorder: MediaRecorder | null = null;
let audioChunks: Blob[] = [];

//初始化url
let baseURL = '';
onBeforeMount(() => {
  if (stateStore.baseUrl == "0") {
    ErrorPop("Please set an url", 5000)
  }
  baseURL = stateStore.baseUrl;


});


// 切换语音识别状态
const toggleVoiceRecognition = () => {
  if (isRecording.value) {
    // 如果正在监听，停止识别
    stopRecording();
    console.log("停止语音识别...");
  } else {
    // 如果未在监听，启动识别
    startRecording();
    console.log("开始语音识别...");
  }
};

// 开始录音
const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});
    audioChunks = []; // 清空之前的音频数据
    isRecording.value = true;

    // 创建 MediaRecorder 进行音频录制
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, {type: 'audio/wav'});
      sendAudioToApi(audioBlob); // 发送到 API
    };

    mediaRecorder.start();
  } catch (error) {
    console.error("无法访问麦克风:", error);
    ErrorPop("Microphone access failed");
  }
};

// 停止录音
const stopRecording = () => {
  if (mediaRecorder) {
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
    isRecording.value = false;
  }
};

// 发送音频到 API
const sendAudioToApi = async (audioBlob: any) => {
  isLoading.value = true;
  result.value = "";

  // 创建 FormData 对象
  const form = new FormData();
  form.append("language", "en");
  form.append("ignore_timestamps", "true");
  form.append("audio", audioBlob, "recording.wav");

  // 配置 fetch 选项
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 7000); // 10秒后中止请求

  const options = {
    method: 'POST',
    headers: {
      Authorization: '',
    },
    body: form,
    signal: controller.signal, // 将 AbortController 的 signal 传递给 fetch
  };

  // 发送请求
  try {
    const response = await fetch(baseURL + '/speech/text', options);
    clearTimeout(timeoutId); // 请求完成前清除定时器
    const data = await response.json();
    result.value = data.text || ErrorPop("No voice input detected"); // 假设 API 返回的识别文本字段是 text
    console.log(result.value);
    inputValue.value += data.text;
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error("请求超时:", error);
      ErrorPop("Request timed out");
    } else {
      console.error("请求失败:", error);
      ErrorPop("Unrecognized");
    }
  } finally {
    isLoading.value = false;
  }
};


//选择音频类型
let audioType = ref("De");

function handleCommand(command: string) {
  console.log('Selected:', command);
  audioType.value = command;
  stateStore.setaudioType(command);
}

// 拖动框的逻辑
interface Position {
  x: number;
  y: number;
}

interface Offset {
  x: number;
  y: number;
}

const position = reactive<Position>({x: window.innerWidth - 900, y: window.innerHeight - 150}) // 初始位置
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
</script>


<style scoped>
.draggable-container {
  display: flex;
  align-items: center;
  width: 600px;
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

.dropdown-button {
  margin-left: 10px; /* 根据需求调整间距，例如10px */
}
</style>