<template>
  <!--  对话页面-->
  <div class="chat-page" ref="chatContainer">
    <!--    对话框-->
    <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-item"
        :class="message.isUser ? 'user-message' : 'ai-message'"
    >

      <div class="avatar" @dblclick="deleteMessage(index)">
        <img v-if="message.isUser" :src="userAvatar" alt="Image"/>
        <img v-else :src="aiAvatar" alt="Image"/>
      </div>

      <div class="message-content">
        <!--        <div v-loading="message.loading" element-loading-background="rgba(255, 255, 255, 0.8)">-->
        <!-- 加载替换 -->
        <div v-if="message.loading" class="loading-text-gradient">
          生成中...
        </div>

        <!-- 消息 -->
        <div v-else>
          <div v-if="!message.isUser" class="message-text markdown-body" v-html="renderedText(message.text)"></div>
          <div v-else class="message-text">
            <div v-if="message.isPicture">
              <img :src="message.text" alt="舌头图片"
                   style="width: 200px; border: 1px solid #ddd; border-radius: 10px;"/>
            </div>

            <div v-else>
              {{ message.text }}
            </div>
          </div>

        </div>
        <div class="message-time">{{ message.time }}
          <!-- 添加语音播放按钮 -->
          <button v-if="!message.isUser && !message.loading" class="speech-button right-aligned"
                  @click="fetchAndPlayAudio(message.text)">🔊
            播放音频
          </button>


        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
// 一再接受inputValue
import {nextTick, onBeforeMount, onMounted, ref, watch} from 'vue';
import MarkdownIt from 'markdown-it'; //渲染markdown
import hljs from 'highlight.js'; // 引入代码高亮库
import 'github-markdown-css';
import {useStateStore} from "@/stores/stateStore"; //状态获取
import 'highlight.js/styles/github.css'; // 确保引入样式文件
import axios from 'axios';
import emojiRegex from 'emoji-regex'; //去除emoji
import {ElMessage} from "element-plus";

const sessionId = ref() //会话id


//初始化图片和解答
const initPage = (basePic, sessionName) => {
  messages.value.push({
    text: basePic.base64,
    isUser: true,
    time: new Date().toLocaleString('default', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }),
    loading: false,
    isPicture: true
  });
  getPictureAnswer(basePic.fileData, sessionName);

}

//后端返回的数据注入
const inputData = (data, id) => {
  // console.log(id)
  sessionId.value = id;
  messages.value = data;
  setTimeout(() => {
    scrollToBottom()
  }, 500)

}


//获取记录
async function getRecordData() {
  try {
    const response = await axios.get('/user/record', {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      }
    });
    console.log(response.data.data[response.data.data.length - 1].state); // 返回后端返回的数据
  } catch (error) {
    console.error('获取 /user/record 失败:', error);
    return null; // 失败时返回 null
  }
}

//重置全部
const resetPage = () => {
  messages.value = [
    {
      text: "# 👋 欢迎来到 **AI 中医舌诊**！\n" +
          "\n" +
          "📸 **请首先上传您的舌像图片**，AI 将根据中医理论进行智能分析，提供健康建议。\n" +
          "\n" +
          "🔍 **如何拍摄舌像？**\n" +
          "1. 在自然光下拍摄，避免过暗或过亮。\n" +
          "2. 放松舌头，尽量伸出，不要用力。\n" +
          "3. 保持清洁，避免食物残留影响判断。\n" +
          "\n" +
          "💡 **免责声明**  \n" +
          "本系统提供的分析结果仅供参考，不能替代专业医生的诊断，如有健康问题，请咨询中医师或专业医生。\n" +
          "\n" +
          "➡ **请上传舌像，让我们开始吧！**\n",
      isUser: false,
      time: new Date().toLocaleString('default', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }),
      loading: false,
      isPicture: false
    }
  ];
}

defineExpose({initPage, inputData, resetPage})


// 使用 ref 定义响应式变量
const userAvatar = ref("./static/userDefault.jpg");  // 用户头像
const aiAvatar = ref("./static");      // AI 头像
const messages = ref([
  {
    text: "# 👋 欢迎来到 **AI 中医舌诊**！\n" +
        "\n" +
        "📸 **请首先上传您的舌像图片**，AI 将根据中医理论进行智能分析，提供健康建议。\n" +
        "\n" +
        "🔍 **如何拍摄舌像？**\n" +
        "1. 在自然光下拍摄，避免过暗或过亮。\n" +
        "2. 放松舌头，尽量伸出，不要用力。\n" +
        "3. 保持清洁，避免食物残留影响判断。\n" +
        "\n" +
        "💡 **免责声明**  \n" +
        "本系统提供的分析结果仅供参考，不能替代专业医生的诊断，如有健康问题，请咨询中医师或专业医生。\n" +
        "\n" +
        "➡ **请上传舌像，让我们开始吧！**\n",
    isUser: false,
    time: new Date().toLocaleString('default', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }),
    loading: false,
    isPicture: false
  }]);
//loading用来记录是否正在加载

let newMessage = ref(''); //发送的数据
const chatContainer = ref(null); //聊天框对象
// 获取 Pinia Store
const stateStore = useStateStore();


// 初始化 MarkdownIt 实例，并启用代码高亮功能
const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, {language: lang}).value}</code></pre>`;
      } catch (__) {
      }
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

// 去除emoji和markdown
function org(input) {
  // 移除 Markdown 标记
  const noMarkdown = input
      .replace(/!\[.*?\]\(.*?\)/g, '')  // 移除图片标记
      .replace(/\[(.*?)\]\(.*?\)/g, '$1')  // 移除链接标记，只保留链接文本
      .replace(/[`_*~#>]/g, '')  // 移除其他 Markdown 符号
      .replace(/\n+/g, ' ');  // 将换行替换为空格

  // 移除 Emoji
  const regex = emojiRegex();
  return noMarkdown.replace(regex, '')
}


// 发送用户消息
const sendMessage = async () => {

  if (newMessage.value.trim() !== '') {
    // 用户信息推入
    messages.value.push({
      text: newMessage.value,
      isUser: true,
      time: new Date().toLocaleString('default', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }),
      loading: false,
      isPicture: false
    });
    //保存
    saveHistory();
    await nextTick();
    scrollToBottom();
    await sendAIMessage(); //  AI 回复
  }
};

// AI 回复
const sendAIMessage = async () => {
  setTimeout(async () => {
    // ai信息推入
    messages.value.push({
      text: '',
      isUser: false,
      time: new Date().toLocaleString('default', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }),
      loading: true,
      isPicture: false
    });
    await scrollToBottom();
    await getAnswer();
    await nextTick();

  }, 500);
};


const getAnswer = async () => {
  const timeout = 10000; // 设置超时时间（以毫秒为单位，例如10秒）

  // 从 localStorage 获取 token
  let token = localStorage.getItem('token');

  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    scrollToBottom();

    const response = await Promise.race([
      fetch(baseURL + "/" + sessionId.value, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` // 添加 Authorization 头
        },
        body: JSON.stringify({
          input: personalPrompt + newMessage.value,
        }),
      }),
      timeoutPromise, // 如果 fetch 未完成，此 promise 将优先返回超时错误
    ]);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    if (!response.body) {
      throw new Error("流式返回没有body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;

    messages.value[messages.value.length - 1].loading = false; // 解除加载

    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        // 解码数据块并按行分割
        // console.log("value", value);
        const chunk = decoder.decode(value, {stream: true});
        // console.log("chunk", chunk);
        const lines = chunk.split("\n");

        // 逐行解析并处理
        lines.forEach((line) => {
          if (line.trim()) { // 忽略空行
            try {
              const parsedChunk = JSON.parse(line);
              if (!parsedChunk.is_complete)
                messages.value[messages.value.length - 1].text += parsedChunk.token;
              scrollToBottom();
            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            }
          }
        });
      }
    }

    scrollToBottom();
    console.log("流结束");
  } catch (error) {
    console.error("错误: ", error);
    messages.value.pop(); // 直接删去最后一个
    if (error.message === "请求超时") {
      ErrorPop("请求超时，请重试");
    } else {
      ErrorPop("出错请重试");
    }
  }
  // 保存
  saveHistory();
};

function logFormData(formData) {
  for (let pair of formData.entries()) {
    console.log(pair[0] + ':', pair[1]);
  }
}

//图片专用传输线路
const getPictureAnswer = async (fileData, sessionName) => {
  emit("get-return", {success: false});
  setTimeout(async () => {
    // ai信息推入
    messages.value.push({
      text: '',
      isUser: false,
      time: new Date().toLocaleString('default', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }),
      loading: true,
      isPicture: false
    });
    await nextTick();
  }, 0);
  const timeout = 15000; // 设置超时时间（以毫秒为单位，例如10秒）

  // 从 localStorage 获取 token
  let token = localStorage.getItem('token');

  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    const response = await Promise.race([
      (async () => {
        const formData = new FormData();
        formData.append('file_data', fileData);
        formData.append('user_input', "描述一下");
        formData.append('name', sessionName);
        logFormData(formData);

        return await fetch(baseURL, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`
          },
          body: formData,
        });
      })(),
      timeoutPromise, // 如果 fetch 未完成，此 promise 将优先返回超时错误
    ]);


    if (!response.ok) {
      // ErrorPop("出错请重试");
      emit("get-return", {success: false});

      throw new Error(`HTTP error! status: ${response.status}`);
    }

    if (!response.body) {
      throw new Error("流式返回没有body");
    }
    emit("get-return", {success: true});

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;

    messages.value[messages.value.length - 1].loading = false; // 解除加载

    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        // 解码数据块并按行分割
        // console.log("value", value);
        const chunk = decoder.decode(value, {stream: true});
        // console.log("chunk", chunk);
        const lines = chunk.split("\n");

        // 逐行解析并处理
        lines.forEach((line) => {
          if (line.trim()) { // 忽略空行
            try {
              const parsedChunk = JSON.parse(line);
              if (!parsedChunk.is_complete)
                messages.value[messages.value.length - 1].text += parsedChunk.token;
              sessionId.value = parsedChunk.session_id;
              emit("back-id", sessionId.value);
              scrollToBottom();
            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            }
          }
        });
      }
    }

    scrollToBottom();
    console.log("流结束");
  } catch (error) {
    emit("get-return", {success: false});
    console.error("错误: ", error);
    messages.value.pop(); // 直接删去最后一个
    if (error.message === "请求超时") {
      ErrorPop("请求超时，请重试");
    } else {
      ErrorPop("出错请重试");
    }
  }
};


//传输图片时回传id
const getPictureId = () => {
  return sessionId.value;
}

//返回markdown
const renderedText = (text) => {
  return md.render(text);
};


// 滚动到底部
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};


//音频类型监听
let audioType = "De";
watch(
    () => stateStore.audioType,
    (newValue, oldValue) => {
      audioType = newValue;
    }
);

const isPlaying = ref(false); // 记录是否正在播放

// 请求播放音频功能
const fetchAndPlayAudio = async (text) => {
  text = org(text); // 处理文本

  if (audioType === "De") {
    if (isPlaying.value) {
      stopAudio(); // 如果正在播放，则停止播放
    } else {
      playAudio(text);
    }
  }
};

const voices = ref([]); // 存储可用的语音列表

// 加载可用的语音
const loadVoices = () => {
  voices.value = window.speechSynthesis.getVoices().filter(voice => voice.lang.startsWith("zh"));
};

onMounted(() => {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices; // 监听语音列表变化
});

// 停止当前正在播放的音频
const stopAudio = () => {
  window.speechSynthesis.cancel();
  isPlaying.value = false; // 更新播放状态
};

const playAudio = (text) => {
  if (!text) {
    return;
  }

  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);

  // 设置语言为中文
  utterance.lang = "zh-CN";

  // 选择音色，确保数组索引不越界
  if (voices.value.length > 6) {
    utterance.voice = voices.value[6];
  }

  // 监听播放开始和结束事件
  utterance.onstart = () => {
    isPlaying.value = true;
  };

  utterance.onend = () => {
    isPlaying.value = false;
  };

  utterance.onerror = () => {
    isPlaying.value = false;
  };

  // 播放音频
  synth.speak(utterance);
};


//头像载入和音频初始化和url初始化
let baseURL = ""
let personalPrompt = ""
onBeforeMount(() => {
  aiAvatar.value = stateStore.aiImagePath;
  userAvatar.value = stateStore.userImagePath;
  stateStore.setaudioType("De"); //先设置成默认音频
  baseURL = stateStore.baseUrl; //先设置成默认url
  personalPrompt = stateStore.personalPrompt;//个人prompt

  //初始化消息记录
  // if (stateStore.chatHistory.length !== 0) messages.value = stateStore.chatHistory;

});

//记录信息
const saveHistory = () => {
  stateStore.setChatHistory(messages.value);
}


// 接收来自父组件的 props
const props = defineProps({
  receivedInput: String
});

// 监听 props 的变化
watch(() => props.receivedInput[0], (newValue) => {
  if (newValue !== undefined) {
    const firstValue = props.receivedInput.slice(2); // 获取第2个值
    handleReceivedInput(firstValue); // 对第2个值进行操作
  }
});


// 处理收到的数据
const handleReceivedInput = (inputValue) => {
  // console.log('子组件main处理收到的数据:', inputValue);
  newMessage.value = inputValue;
  sendMessage();
};

//错误弹窗
const ErrorPop = (info, time = 3000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'error',
    duration: time
  })
}

//音频的互动ui逻辑


//成功弹窗
const SuccessPop = (info, time = 2000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'success',
    duration: time
  })
}

// 删除消息
const deleteMessage = (index) => {
  messages.value.splice(index, 1);
  //保存
  saveHistory();
};

const emit = defineEmits(['get-return', 'back-id']);

</script>

<style scoped>

.chat-page {
  display: flex;
  flex-direction: column;
  padding: 0px;
  margin-top: 20px; /* 让容器与顶部保持距离 */
  height: calc(100vh - 100px); /* 调整高度，以适应新的margin-top */
  overflow-y: auto;
  flex-grow: 1;
  scroll-behavior: smooth;
}


.message-item {
  display: flex;
  align-items: flex-end;
  margin-bottom: 10px;
}

.user-message {
  flex-direction: row-reverse;
  text-align: left;
}

.ai-message {
  flex-direction: row;
}

.avatar {
  width: 40px;
  height: 40px;
  margin: 0 10px;
}

.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.message-content {
  max-width: 60%;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', 'Helvetica', sans-serif; /* 设置字体 */
  font-size: 16px; /* 字体大小 */
  line-height: 1.0; /* 行间距，使内容更易读 */
  color: #333; /* 字体颜色 */
}

.user-message .message-content {
  background-color: #8fefdd;
}

.ai-message .message-content {
  font-size: 100px; /* AI 回复字体大小 */
}

.message-time {
  font-size: 12px;
  color: #888;
  margin-top: 7px;
}

.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 15px;
}

@media (max-width: 767px) {
  .markdown-body {
    padding: 15px;
  }
}

.loading-text-gradient {
  font-size: 18px; /* 字体大小 */

  font-family: 'Times New Roman', serif; /* 使用 Times New Roman 字体 */
  font-style: italic; /* 设置斜体 */
  position: relative;
  color: #c0c0c0; /* 设置较暗的文字颜色作为背景 */
  overflow: hidden; /* 确保动画在边界内 */
  padding-bottom: 5px; /* 只向下增加5px的内边距 */

}

.loading-text-gradient::before {
  content: "生成中...";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, rgba(0, 0, 255, 0.1), rgb(255, 255, 255), rgba(0, 0, 255, 0.1)); /* 改为蓝色渐变 */
  background-size: 1000% 100%; /* 增加背景大小以拉宽光条的效果 */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3.0s ease-in-out infinite; /* 缩短动画时间并使用 ease-in-out 效果，使得动画看起来更顺滑 */
}

@keyframes shine {
  0% {
    background-position: -150% 0; /* 光条从更远的左边开始 */
  }
  100% {
    background-position: 150% 0; /* 光条移动到更远的右边 */
  }
}

.speech-button.right-aligned {
  float: right;
  margin-left: 10px;
  font-size: 12px;
  color: #888;
  background: none;
  border: none;
  cursor: pointer;
}

</style>
