<template>
  <el-steps style="max-width: 2000px" :active="active" finish-status="success" align-center>
    <el-step title="上传图像" />
    <el-step title="图像诊断中" />
    <el-step title="结果完成" />
  </el-steps>

  <h1 class="tips">等待结果约30s左右</h1>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref(0)

active.value = 2
</script>

<style>
  .tips {
    position: relative;
    text-align: center;
    color: #00bd7e;
  }
</style>
