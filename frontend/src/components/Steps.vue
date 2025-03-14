<template>
  <div class="countdown-container">
    <!-- SVG 计时条容器 -->
    <svg width="300" height="180" viewBox="0 0 200 100" class="countdown-svg">
      <!-- 灰色背景矩形 -->
      <rect x="10" y="10" width="180" height="80" rx="15" ry="15" stroke="#ddd" fill="none" stroke-width="5"/>
      <!-- 进度条矩形，颜色和长度随时间变化 -->
      <rect
          x="10"
          y="10"
          width="180"
          height="80"
          rx="15"
          ry="15"
          :stroke="barColor"
          fill="none"
          stroke-width="5"
          stroke-dasharray="520"
          :stroke-dashoffset="totalLength - dashOffset"
          stroke-linecap="round"
          style="transition: stroke 1s ease, stroke-dashoffset 1s linear;"
      />
      <!-- 显示剩余时间，居中对齐 -->
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" class="countdown-text">{{
          remainingTime
        }}s
      </text>
    </svg>
    <!-- 重置按钮 -->
    <!--    <button class="reset-button" @click="resetCountdown">重置</button>-->
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';

const totalTime = 20; // 总倒计时时间（秒）
const remainingTime = ref(totalTime); // 剩余时间
const dashOffset = ref(0); // 进度条偏移量
const totalLength = 520; // 矩形路径的总长度
let interval; // 计时器引用

// 根据剩余时间计算进度条颜色
const barColor = computed(() => {
  const percentage = remainingTime.value / totalTime;
  if (percentage > 0.66) return '#ff0000'; // 红色（高时间）
  if (percentage > 0.33) return '#ffcc00'; // 黄色（中时间）
  return '#4caf50'; // 绿色（低时间）
});

// 启动倒计时
const startCountdown = () => {
  interval = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--;
      dashOffset.value = (1 - remainingTime.value / totalTime) * totalLength;
    } else {
      clearInterval(interval);
    }
  }, 1000);
};

// 重置倒计时
const resetCountdown = () => {
  clearInterval(interval);
  remainingTime.value = totalTime; // 重置剩余时间
  dashOffset.value = 0; // 重置进度条
  startCountdown(); // 重新启动倒计时
};

defineExpose({startCountdown, resetCountdown})
</script>

<style scoped>
.countdown-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: relative;
}

.countdown-svg {
  position: relative;
}

.countdown-text {
  font-size: 18px;
  font-weight: bold;
  fill: black;
}

.reset-button {
  margin-top: 10px;
  padding: 5px 10px;
  font-size: 16px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 5px;
}

.reset-button:hover {
  background-color: #0056b3;
}
</style>
