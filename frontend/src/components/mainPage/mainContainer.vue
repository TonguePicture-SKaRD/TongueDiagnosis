<script setup lang="ts">
import Bottom from "./dialogBox.vue";
import Main from "./main.vue";
import {ref} from 'vue'

let sharedInput = ref('');
const mainRef = ref(null)
const dialogRef = ref(null)
const tempName = ref('')

const handleSendToMain = (id: number, input: string) => {
  sharedInput.value = `${id},${input}`;
};

const handleSendPicture = (info) => {
  initPage(info, tempName.value);
};

const initPage = (basePic, sessionName) => {
  mainRef.value.initPage(basePic, sessionName);
}

const inputData = (data, id) => {
  dialogRef.value.startChat()
  mainRef.value.inputData(data, id);
}

const resetPage = () => {
  mainRef.value.resetPage();
  dialogRef.value.backUploading();
}

const setTempName = (name) => {
  console.log(name);
  tempName.value = name;
}

defineExpose({inputData, resetPage, setTempName})

const handleGetReturn = (data) => {
  dialogRef.value.getReturn(data);
}

const backIdToCheck = (id) => {
  emit("back-id", id);
}

const emit = defineEmits(["back-id"])
</script>

<template>
  <div class="back-ground">
    <div class="common-layout">
      <Main :receivedInput="sharedInput" ref="mainRef" @get-return="handleGetReturn" @back-id="backIdToCheck"/>
      <Bottom @send-to-main="handleSendToMain" @send-picture="handleSendPicture" ref="dialogRef"/>
    </div>
  </div>
</template>

<style scoped>
.back-ground {
  height: 80vh;
  background: linear-gradient(135deg, #4facfe, rgba(90, 224, 231, 0.9), #00d4a9, #00cba9);
  background-size: 200% 200%;
}
</style>