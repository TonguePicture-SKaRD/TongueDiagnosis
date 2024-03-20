<template>
  <div class="card" v-for="item in rec" :key="rec.id">
    <el-descriptions
        title="Result"
        direction="vertical"
        :column="4"
        :size="size"
        border
    >
      <el-descriptions-item label="图片">
        <el-tag size="small"><router-link :to=item.img_src>点击查看</router-link></el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="检测结果"
      >{{color[item.result.tongue_color]}}，{{outcolor[item.result.coating_color]}}，{{rot[item.result.rot_greasy]}}，{{thick[item.result.tongue_thickness]}}
      </el-descriptions-item>
    </el-descriptions>
  </div>
</template>
<script setup>
  import axios from "axios";
  import { ref, onMounted } from 'vue'

  const color = {
    [0]: "淡白舌",
    [1]: "淡红舌",
    [2]: "红舌",
    [3]: "绛舌",
    [4]: "青紫舌",
  }
  const outcolor = {
    [0]: "白苔",
    [1]: "黄苔",
    [2]: "灰黑苔",
  }
  const rot = {
    [0]: "腻",
    [1]: "腐",
  }
  const thick = {
    [0]: "薄",
    [1]: "厚",
  }
  function reverseArray1(arr) {
    for (let index = 0; index < Math.floor(arr.length / 2); index++) {
      // 借助第三方变量交换两个变量的值
      let temp = arr[index];
      arr[index] = arr[arr.length - 1 - index];
      arr[arr.length - 1 - index] = temp
    }
    return arr;
  }
  let rec = ref([]);
  onMounted(function () {
    const timer = window.setInterval(() => {
      setTimeout(function () {
        axios.get("/user/record", {
        })
        .then(function(res) {
          console.log(res.data)
          rec.value = res.data.data
          reverseArray1(rec.value)
          console.log(rec.value)
          console.log(rec.value[1].state)
        })
        .catch(function(error) {
          console.log(error);
        })
        .then(res => {
          //视情况而定
          if (rec.value[0].state === 1) {
            // 这里可以写一些中止轮询的条件 比如code值返回0时
            clearInterval(timer)
          }
        })
      }, 0)
    }, 2000)
    // 清除定时器
    // this.$once('hook:beforeDestroy', () => {
    //   clearInterval(timer)
    // })
  });

</script>
