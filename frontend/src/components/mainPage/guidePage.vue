<template>
  <!-- 主容器 -->
  <div class="main-container">
    <!-- 欢迎界面 -->


    <div v-if="showWelcome" class="welcome-container">
      <div class="content-wrapper">
        <div class="icon-box">
          <!--          <i class="fas fa-comment-medical floating-icon"></i>-->
          <img src="@\assets\Chat_Tongue.webp" alt="" class="fas fa-comment-medical floating-icon"
               style="height: 20vh;border-radius: 50%;">
          <!--          <i class="fas fa-arrow-left guide-arrow"></i>-->
        </div>

        <div class="text-content">
          <h1 class="title">欢迎开启AI舌诊之旅 👋</h1>
          <p class="subtitle">点击左侧{{ guideText }}<br>获取中医舌象分析</p>
        </div>
      </div>

      <div class="decorations">
        <div class="circle c1"></div>
        <div class="circle c2"></div>
        <div class="circle c3"></div>
      </div>
    </div>

    <!-- 右侧提示 -->
    <div v-if="showWelcome" class="right-prompt">
      <div class="prompt-box">
        <i class="fas fa-hand-point-left"></i>
        <span>点击这边添加或查看对话</span>
      </div>
    </div>

  </div>
</template>

<script setup>
import {ref} from 'vue'

const showWelcome = ref(true)
const guideText = ref('')

const handleChatStart = () => {
  showWelcome.value = false
}

const changeGuideText = (text) => {
  guideText.value = text
}

defineExpose({handleChatStart, changeGuideText})
</script>

<style scoped>
/* 主容器样式 */
.main-container {
  position: relative;
  flex: 1;
  height: 100%;
  overflow: hidden;
}

/* 欢迎界面样式 */
.welcome-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f0f9ff 0%, #fdf2ff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.content-wrapper {
  text-align: center;
  position: relative;
  z-index: 2;
}

.icon-box {
  position: relative;
  margin-bottom: 2rem;
}

.fa-comment-medical {
  font-size: 8rem;
  color: #6366f1;
  filter: drop-shadow(0 4px 6px rgba(79, 70, 229, 0.15));
}

/* 动画效果 */
.floating-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 文字样式 */
.title {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.subtitle {
  font-size: 1.25rem;
  color: #4b5563;
  line-height: 1.75rem;
}

/* 装饰元素 */
.decorations .circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.4;
}

.c1 {
  width: 200px;
  height: 200px;
  background: #818cf8;
  top: 20%;
  left: 10%;
}

.c2 {
  width: 300px;
  height: 300px;
  background: #f472b6;
  bottom: 15%;
  right: 10%;
}

.c3 {
  width: 150px;
  height: 150px;
  background: #38bdf8;
  top: 50%;
  left: 30%;
}

/* 右侧提示 */
.right-prompt {
  position: absolute;
  left: 2rem;
  top: 10%;
  transform: translateY(-50%);
  z-index: 101;
}

.prompt-box {
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: slideIn 4s ease-out, hover-shake 2s ease-in-out infinite;;
}


/* 响应式设计 */
@media (max-width: 768px) {
  .fa-comment-medical {
    font-size: 5rem !important;
  }

  .title {
    font-size: 1.8rem !important;
  }

  .guide-arrow {
    display: none;
  }

  .right-prompt {
    display: none;
  }
}


.guide-arrow {
  position: absolute;
  left: -80px;
  top: 50%;
  font-size: 3rem;
  color: #f472b6;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: translateX(0);
  }
  50% {
    opacity: 0.5;
    transform: translateX(-10px);
  }
}

/* 新增晃动动画 */
@keyframes hover-shake {
  0%, 100% {
    transform: translateY(-50%) translateX(0);
  }
  25% {
    transform: translateY(-50%) translateX(5px);
  }
  75% {
    transform: translateY(-50%) translateX(-5px);
  }
}

/* 调整原有进入动画 */
@keyframes slideIn {
  from {
    transform: translateY(-50%) translateX(100%);
  }
  to {
    transform: translateY(-50%) translateX(0);
  }
}
</style>