<template>
  <el-steps style="max-width: 2000px" :active="active" finish-status="success" align-center>
    <el-step title="Step 1" />
    <el-step title="Step 2" />
    <el-step title="Step 3" />
  </el-steps>

  <h1 class="tips">等待结果约30s左右</h1>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref(0)

const next = () => {
  if (active.value++ > 2) active.value = 0
}
</script>

<style>
  .tips {
    position: relative;
    text-align: center;
    color: #00bd7e;
  }
</style>
