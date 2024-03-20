<template>
  <UploadPicture v-if="isUpload === 0" :isupload="isUpload"></UploadPicture>
  <Steps v-if="isUpload === 1"></Steps>
</template>

<script setup>
  import { ref} from "vue";

  let isUpload = ref(0);
  import UploadPicture from "@/components/UploadPicture.vue";
  import Steps from "@/components/Steps.vue";
</script>