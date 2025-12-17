<script setup>
import {nextTick, onBeforeMount, onMounted, ref, watch} from 'vue';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import 'github-markdown-css';
import {useStateStore} from "@/stores/stateStore";
import 'highlight.js/styles/github.css';
import axios from 'axios';
import emojiRegex from 'emoji-regex';
import {ElMessage} from "element-plus";

const sessionId = ref()

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

const inputData = (data, id) => {
  sessionId.value = id;
  messages.value = data;
  setTimeout(() => {
    scrollToBottom()
  }, 500)

}

async function getRecordData() {
  try {
    const response = await axios.get('/user/record', {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      }
    });
    console.log(response.data.data[response.data.data.length - 1].state);
  } catch (error) {
    console.error('获取 /user/record 失败:', error);
    return null;
  }
}

const resetPage = () => {
  messages.value = [
    {
      text: "# 👋 Welcome to  **AI Tongue Diagnosis**！\n" +
          "\n" +
          "📸 **Please first upload your tongue image.**，AI will conduct intelligent analysis based on traditional Chinese medicine theory and provide health advice.\n" +
          "\n" +
          "🔍 **How to take a picture of the tongue?**\n" +
          "1. Shoot in natural light to avoid being too dark or too bright.\n" +
          "2. Relax your tongue and stretch it out as far as possible. Don't exert any force.\n" +
          "3. Keep clean to avoid food residue affecting your judgment.\n" +
          "\n" +
          "💡 **Disclaimer**  \n" +
          "The analysis results provided by this system are for reference only and cannot replace the diagnosis made by a professional doctor. If you have any health issues, please consult a traditional Chinese medicine doctor or a professional medical expert.\n" +
          "\n" +
          "➡ **Please upload your tongue image and let's get started!**\n",
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

const userAvatar = ref("./static/userDefault.jpg");
const aiAvatar = ref("./static");
const messages = ref([
  {
    text: "# 👋 Welcome to  **AI Tongue Diagnosis**！\n" +
        "\n" +
        "📸 **Please first upload your tongue image.**，AI will conduct intelligent analysis based on traditional Chinese medicine theory and provide health advice.\n" +
        "\n" +
        "🔍 **How to take a picture of the tongue?**\n" +
        "1. Shoot in natural light to avoid being too dark or too bright.\n" +
        "2. Relax your tongue and stretch it out as far as possible. Don't exert any force.\n" +
        "3. Keep clean to avoid food residue affecting your judgment.\n" +
        "\n" +
        "💡 **Disclaimer**  \n" +
        "The analysis results provided by this system are for reference only and cannot replace the diagnosis made by a professional doctor. If you have any health issues, please consult a traditional Chinese medicine doctor or a professional medical expert.\n" +
        "\n" +
        "➡ **Please upload your tongue image and let's get started!**\n",
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

let newMessage = ref('');
const chatContainer = ref(null);
const stateStore = useStateStore();

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

function org(input) {
  const noMarkdown = input
      .replace(/!\[.*?\]\(.*?\)/g, '')
      .replace(/\[(.*?)\]\(.*?\)/g, '$1')
      .replace(/[`_*~#>]/g, '')
      .replace(/\n+/g, ' ');
  const regex = emojiRegex();
  return noMarkdown.replace(regex, '')
}

const sendMessage = async () => {
  if (newMessage.value.trim() !== '') {
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
    saveHistory();
    await nextTick();
    scrollToBottom();
    await sendAIMessage();
  }
};

const sendAIMessage = async () => {
  setTimeout(async () => {
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
      isPicture: false,
      receivedContent: false // 标记是否已接收到内容
    });
    await scrollToBottom();
    await getAnswer();
    await nextTick();
  }, 500);
};


const getAnswer = async () => {
  const timeout = 40000;
  let token = localStorage.getItem('token');
  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    scrollToBottom();
    console.log(baseURL + "/" + sessionId.value);
    const response = await Promise.race([
      fetch(baseURL + "/" + sessionId.value, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          input: personalPrompt + newMessage.value,
        }),
      }),
      timeoutPromise,
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

    // 不立即解除加载，而是保持Thinking状态直到收到第一块数据

    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        const chunk = decoder.decode(value, {stream: true});
        const lines = chunk.split("\n");
        lines.forEach((line) => {
          if (line.trim()) {
            try {
              const parsedChunk = JSON.parse(line);
              if (!parsedChunk.is_complete && parsedChunk.token) {
                // 第一次收到有效token时，才停止thinking状态
                const currentMessage = messages.value[messages.value.length - 1];
                if (!currentMessage.receivedContent) {
                  currentMessage.receivedContent = true;
                  currentMessage.loading = false; // 解除加载
                }
                currentMessage.text += parsedChunk.token;
              }
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
    // 错误时停止最后一条消息的加载状态
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].loading) {
      const currentMessage = messages.value[messages.value.length - 1];
      currentMessage.loading = false;
      // 如果没有接收到内容，标记为已接收，这样就不会在UI上显示空白
      if (!currentMessage.receivedContent) {
        currentMessage.receivedContent = true;
      }
    }
    messages.value.pop(); // 直接删去最后一个
    if (error.message === "请求超时") {
      ErrorPop("Request timeout. Please try again.");
    } else {
      ErrorPop("Encounter an error, please try again.");
    }
  }
  saveHistory();
};

function logFormData(formData) {
  for (let pair of formData.entries()) {
    console.log(pair[0] + ':', pair[1]);
  }
}

const getPictureAnswer = async (fileData, sessionName) => {
  emit("get-return", {success: false});
  setTimeout(async () => {
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
      isPicture: false,
      receivedContent: false // 标记是否已接收到内容
    });
    await nextTick();
  }, 0);
  const timeout = 40000;

  let token = localStorage.getItem('token');

  const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    const response = await Promise.race([
      (async () => {
        const formData = new FormData();
        formData.append('file_data', fileData);
        formData.append('user_input', "Descript it");
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
      timeoutPromise,
    ]);


    if (!response.ok) {
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

    // 不立即解除加载，而是保持Thinking状态直到收到第一块数据

    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;

      if (value) {
        const chunk = decoder.decode(value, {stream: true});
        const lines = chunk.split("\n");

        lines.forEach((line) => {
          if (line.trim()) {
            try {
              const parsedChunk = JSON.parse(line);
              if (!parsedChunk.is_complete && parsedChunk.token) {
                // 第一次收到有效token时，才停止thinking状态
                const currentMessage = messages.value[messages.value.length - 1];
                if (!currentMessage.receivedContent) {
                  currentMessage.receivedContent = true;
                  currentMessage.loading = false; // 解除加载
                }
                currentMessage.text += parsedChunk.token;
              }
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

    // 确保在流结束时停止最后一条消息的加载状态
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].loading) {
      const currentMessage = messages.value[messages.value.length - 1];
      currentMessage.loading = false;
      // 如果没有接收到内容，标记为已接收，这样就不会在UI上显示空白
      if (!currentMessage.receivedContent) {
        currentMessage.receivedContent = true;
      }
    }
    scrollToBottom();
    console.log("流结束");
  } catch (error) {
    emit("get-return", {success: false});
    console.error("错误: ", error);
    // 错误时停止最后一条消息的加载状态
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].loading) {
      const currentMessage = messages.value[messages.value.length - 1];
      currentMessage.loading = false;
      // 如果没有接收到内容，标记为已接收，这样就不会在UI上显示空白
      if (!currentMessage.receivedContent) {
        currentMessage.receivedContent = true;
      }
    }
    messages.value.pop(); // 直接删去最后一个
    if (error.message === "请求超时") {
      ErrorPop("Request timeout. Please try again.");
    } else {
      ErrorPop("Encounter an error, please try again.");
    }
  }
};

const getPictureId = () => {
  return sessionId.value;
}

const renderedText = (text) => {
  return md.render(text);
};

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

let audioType = "De";
watch(
    () => stateStore.audioType,
    (newValue, oldValue) => {
      audioType = newValue;
    }
);

const isPlaying = ref(false);
const fetchAndPlayAudio = async (text) => {
  text = org(text);

  if (audioType === "De") {
    if (isPlaying.value) {
      stopAudio();
    } else {
      playAudio(text);
    }
  }
};

const voices = ref([]);
const loadVoices = () => {
  voices.value = window.speechSynthesis.getVoices().filter(voice => voice.lang.startsWith("zh"));
};

onMounted(() => {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices;
});

const stopAudio = () => {
  window.speechSynthesis.cancel();
  isPlaying.value = false;
};

const playAudio = (text) => {
  if (!text) {
    return;
  }
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "zh-CN";
  if (voices.value.length > 6) {
    utterance.voice = voices.value[6];
  }
  utterance.onstart = () => {
    isPlaying.value = true;
  };
  utterance.onend = () => {
    isPlaying.value = false;
  };
  utterance.onerror = () => {
    isPlaying.value = false;
  };
  synth.speak(utterance);
};

let baseURL = ""
let personalPrompt = ""
onBeforeMount(() => {
  aiAvatar.value = stateStore.aiImagePath;
  userAvatar.value = stateStore.userImagePath;
  stateStore.setaudioType("De");
  baseURL = stateStore.baseUrl;
  personalPrompt = stateStore.personalPrompt;
});

const saveHistory = () => {
  stateStore.setChatHistory(messages.value);
}

const props = defineProps({
  receivedInput: String
});

watch(() => props.receivedInput[0], (newValue) => {
  if (newValue !== undefined) {
    const firstValue = props.receivedInput.slice(2);
    handleReceivedInput(firstValue);
  }
});

const handleReceivedInput = (inputValue) => {
  newMessage.value = inputValue;
  sendMessage();
};

const ErrorPop = (info, time = 3000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'error',
    duration: time
  })
}

const SuccessPop = (info, time = 2000) => {
  ElMessage({
    showClose: true,
    message: info,
    type: 'success',
    duration: time
  })
}

const deleteMessage = (index) => {
  messages.value.splice(index, 1);
  saveHistory();
};
const emit = defineEmits(['get-return', 'back-id']);
</script>

<template>
  <div class="chat-page" ref="chatContainer">
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
        <div v-if="message.loading" class="loading-text-gradient">
          Thinking...
        </div>
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
          <button v-if="!message.isUser && !message.loading" class="speech-button right-aligned"
                  @click="fetchAndPlayAudio(message.text)">🔊
            Play audio
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  padding: 0px;
  margin-top: 20px;
  height: calc(100vh - 100px);
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
  font-family: 'Arial', 'Helvetica', sans-serif;
  font-size: 16px;
  line-height: 1.0;
  color: #333;
}

.user-message .message-content {
  background-color: #8fefdd;
}

.ai-message .message-content {
  font-size: 100px;
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
  font-size: 18px;
  font-family: 'Times New Roman', serif;
  font-style: italic;
  position: relative;
  color: #c0c0c0;
  overflow: hidden;
  padding-bottom: 5px;
}

.loading-text-gradient::before {
  content: "生成中...";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, rgba(0, 0, 255, 0.1), rgb(255, 255, 255), rgba(0, 0, 255, 0.1));
  background-size: 1000% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3.0s ease-in-out infinite;
}

@keyframes shine {
  0% {
    background-position: -150% 0;
  }
  100% {
    background-position: 150% 0;
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
