<!--<template>-->
<!--  <div class="speech-recognition">-->
<!--    <h1>Speech Recognition Demo</h1>-->
<!--    <p v-if="isListening">🎙️ Listening...</p>-->
<!--    <p v-else>🛑 Not Listening</p>-->
<!--    <p><strong>Recognized Text:</strong> {{ recognizedText }}</p>-->
<!--    <div>-->
<!--      <button @click="startListening" :disabled="isListening">Start Listening</button>-->
<!--      <button @click="stopListening" :disabled="!isListening">Stop Listening</button>-->
<!--      <button @click="clearText">Clear Text</button>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted } from "vue";-->

<!--// State variables-->
<!--const isListening = ref(false);-->
<!--const recognizedText = ref("");-->
<!--let recognition = null;-->

<!--// Lifecycle hook to initialize SpeechRecognition-->
<!--onMounted(() => {-->
<!--  const SpeechRecognition =-->
<!--      window.SpeechRecognition || window.webkitSpeechRecognition;-->
<!--  if (!SpeechRecognition) {-->
<!--    alert("Speech Recognition is not supported in this browser.");-->
<!--    return;-->
<!--  }-->

<!--  // Initialize SpeechRecognition-->
<!--  recognition = new SpeechRecognition();-->
<!--  recognition.lang = "en-US"; // Language-->
<!--  recognition.interimResults = true; // Show interim results-->
<!--  recognition.continuous = true; // Continuous listening-->

<!--  // Recognition event listeners-->
<!--  recognition.onstart = () => {-->
<!--    isListening.value = true;-->
<!--  };-->
<!--  recognition.onresult = (event) => {-->
<!--    const transcript = Array.from(event.results)-->
<!--        .map((result) => result[0].transcript)-->
<!--        .join("");-->
<!--    recognizedText.value = transcript;-->
<!--  };-->
<!--  recognition.onerror = (event) => {-->
<!--    console.error("Recognition error:", event.error);-->
<!--  };-->
<!--  recognition.onend = () => {-->
<!--    isListening.value = false;-->
<!--  };-->
<!--});-->

<!--// Methods-->
<!--const startListening = () => {-->
<!--  if (recognition && !isListening.value) {-->
<!--    recognition.start();-->
<!--  }-->
<!--};-->

<!--const stopListening = () => {-->
<!--  if (recognition && isListening.value) {-->
<!--    recognition.stop();-->
<!--  }-->
<!--};-->

<!--const clearText = () => {-->
<!--  recognizedText.value = "";-->
<!--};-->
<!--</script>-->

<!--<style scoped>-->
<!--.speech-recognition {-->
<!--  max-width: 600px;-->
<!--  margin: 0 auto;-->
<!--  text-align: center;-->
<!--  font-family: Arial, sans-serif;-->
<!--}-->
<!--button {-->
<!--  margin: 5px;-->
<!--  padding: 10px 20px;-->
<!--  border: none;-->
<!--  border-radius: 5px;-->
<!--  cursor: pointer;-->
<!--}-->
<!--button:disabled {-->
<!--  background-color: #ccc;-->
<!--  cursor: not-allowed;-->
<!--}-->
<!--</style>-->
<template>
  <UploadPicture/>
</template>
<script setup>
import UploadPicture from "@/components/TotalUpload.vue";
</script>