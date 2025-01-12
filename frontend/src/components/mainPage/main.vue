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
          Generating...
        </div>

        <!-- 消息 -->
        <div v-else>
          <div v-if="!message.isUser" class="message-text markdown-body" v-html="renderedText(message.text)"></div>
          <div v-else class="message-text">{{ message.text }}</div>
        </div>
        <div class="message-time">{{ message.time }}
          <!-- 添加语音播放按钮 -->
          <button v-if="!message.isUser && !message.loading" class="speech-button right-aligned"
                  @click="fetchAndPlayAudio(message.text)">🔊
            Play Voice
          </button>


        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import {ref, nextTick, computed, onBeforeMount, createCommentVNode} from 'vue';
import MarkdownIt from 'markdown-it'; //渲染markdown
import hljs from 'highlight.js'; // 引入代码高亮库
import 'github-markdown-css';
import {useStateStore} from "@/stores/stateStore.ts"; //状态获取
import 'highlight.js/styles/github.css'; // 确保引入样式文件
import axios from 'axios';
import emojiRegex from 'emoji-regex'; //去除emoji
//图片


// 使用 ref 定义响应式变量
const userAvatar = ref("./static/userDefault.jpg");  // 用户头像
const aiAvatar = ref("./static");      // AI 头像
const messages = ref([{text: 'Who are you？', isUser: true, time: '2024/10/11 16:39', loading: false},
  {
    text: '##  👋 Hi! This is your local AI assistant.\n' +
        '\n' +
        '**You are experiencing a local AI chatbot that is not restricted by the network and can communicate with you anytime, anywhere.**\n' +
        '\n' +
        '**No need to worry about the network connection, no need to use the Internet** As long as you input your ideas or questions, I will do my best to help you.',
    isUser: false,
    time: '2024/10/11 16:39',
    loading: false
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
      time: new Date().toLocaleString(),
      loading: false
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
      loading: true
    });
    await scrollToBottom();
    await getAnswer();
    await nextTick();

  }, 500);
};


const getAnswer = async () => {
  const timeout = 10000; // 设置超时时间（以毫秒为单位，例如10秒）

  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    scrollToBottom();

    const response = await Promise.race([
      fetch(baseURL + "/ai/back", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "gemma2:2b",
          prompt: personalPrompt + newMessage.value,
        }),
      }),
      timeoutPromise, // 如果 fetch 未完成，此 promise 将优先返回超时错误
    ]);

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
        const chunk = decoder.decode(value, {stream: true});
        // console.log("chunk",chunk);
        const lines = chunk.split("\n");

        // 逐行解析并处理
        lines.forEach((line) => {
          if (line.trim()) { // 忽略空行
            try {
              const parsedChunk = JSON.parse(line);
              messages.value[messages.value.length - 1].text += parsedChunk.response;
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
    messages.value.pop(); //直接删去最后一个
    if (error.message === "请求超时") {
      ErrorPop("Timeout");
    } else {
      ErrorPop("404 Warning");
    }
  }
  //保存
  saveHistory();
};


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

// 请求后端并播放音频功能
const fetchAndPlayAudio = async (text) => {
  text = org(text);
  if (audioType === "De") speakMessage(text);
  else {
    SuccessPop("Generating...", 5000);
    const startTime = performance.now();
    try {
      const formData = new FormData();
      formData.append("text", text);
      formData.append("id", audioType);

      const response = await axios.post(baseURL + '/text/speech', formData, {
        responseType: 'blob'  // 指定返回类型为 Blob
      });

      if (!response || response.status !== 200) {
        throw new Error('Failed to fetch audio');
      }

      // 将响应转化为一个声音 Blob
      const audioBlob = response.data;
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      // closeSuccMessage();
      SuccessPop("Playing...")
      audio.play();

      // 监听音频播放结束，释放 Blob URL
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);  // 释放 URL
        console.log('Audio URL revoked');
      };

      const endTime = performance.now();
      console.log(`Audio fetched and played in ${(endTime - startTime).toFixed(2) / 1000} seconds.`);
    } catch (error) {
      console.error('Failed to play audio:', error);
      ErrorPop('Failed to play audio');
    }
  }
};

//前端直接播放
const speakMessage = (text) => {
  console.time("SpeechSynthesis Start Time"); // 开始计时

  const synth = window.speechSynthesis;
  if (synth.speaking) {
    console.error('SpeechSynthesis is already speaking.');
    return;
  }

  if (text !== '') {
    const utterThis = new SpeechSynthesisUtterance(text);
    utterThis.onstart = () => {
      console.timeEnd("SpeechSynthesis Start Time"); // 结束计时并打印耗时
      console.log('SpeechSynthesisUtterance has started speaking.');
    };
    utterThis.onend = () => {
      console.log('SpeechSynthesisUtterance has finished speaking.');
    };
    utterThis.onerror = (event) => {
      console.error('SpeechSynthesisUtterance error: ', event);
    };

    // 选择语音 (可根据需要进行自定义)
    const voices = synth.getVoices();
    utterThis.voice = voices.find(voice => voice.lang === 'en-US') || voices[0];
    synth.speak(utterThis);
  }

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
  if (stateStore.chatHistory.length !== 0) messages.value = stateStore.chatHistory;

});

//记录信息
const saveHistory = () => {
  stateStore.setChatHistory(messages.value);
}

// 一再接受inputValue
import {watch} from 'vue';
import {ElMessage} from "element-plus";


// 接收来自父组件的 props
const props = defineProps({
  receivedInput: String
});

// 监听 props 的变化
watch(() => props.receivedInput[0], (newValue) => {
  if (newValue !== undefined) {
    const firstValue = props.receivedInput[1]; // 获取第2个值
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

//web speech api
// const synth = window.speechSynthesis;
// onBeforeUnmount(() => {
//   synth.cancel(); // 取消任何正在进行的语音播放
// });


</script>

<style scoped>

.chat-page {
  display: flex;
  flex-direction: column;
  padding: 0px;
  margin-top: 20px; /* 让容器与顶部保持距离 */
  height: calc(100vh - 20px); /* 调整高度，以适应新的margin-top */
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
  content: "Generating...";
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
