<script setup>
import {ref, computed, onMounted} from 'vue';

const totalTime = 40;
const remainingTime = ref(totalTime);
const dashOffset = ref(0);
const totalLength = 520;
let interval;

const barColor = computed(() => {
  const percentage = remainingTime.value / totalTime;
  if (percentage > 0.66) return '#ff0000';
  if (percentage > 0.33) return '#ffcc00';
  return '#4caf50';
});

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

const resetCountdown = () => {
  clearInterval(interval);
  remainingTime.value = totalTime;
  dashOffset.value = 0;
  startCountdown();
};

defineExpose({startCountdown, resetCountdown})
</script>

<template>
  <div class="countdown-container">
    <svg width="300" height="180" viewBox="0 0 200 100" class="countdown-svg">>
      <rect x="10" y="10" width="180" height="80" rx="15" ry="15" stroke="#ddd" fill="none" stroke-width="5"/>
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
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" class="countdown-text">{{
          remainingTime
        }}s
      </text>
    </svg>
  </div>
</template>

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
