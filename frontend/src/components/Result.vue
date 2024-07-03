<template>
  <div class="card" v-for="item in rec" :key="rec.id" v-if="isEmpty === true">
    <el-descriptions
        title="Result"
        direction="vertical"
        :column="4"
        :size="size"
        border
    >
      <el-descriptions-item label="图片"  width="450px">
        <el-tag size="small"><a :href=item.img_src>点击查看</a></el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="检测结果" v-if="item.state === 0">
        检测中，请稍等
      </el-descriptions-item>
      <el-descriptions-item label="检测结果" v-if="item.state === 1">
        {{color[item.result.tongue_color]}}{{outcolor[item.result.coating_color]}}{{rot[item.result.rot_greasy]}}{{thick[item.result.tongue_thickness]}}
      </el-descriptions-item>
      <el-descriptions-item label="检测结果" v-if="item.state === 201">
        未检测到舌象，请重新上传清晰舌象
      </el-descriptions-item>
      <el-descriptions-item label="检测结果" v-if="item.state === 202">
        出现多个舌象，请重新拍照上传
      </el-descriptions-item>
      <el-descriptions-item label="检测结果" v-if="item.state === 203">
        文件类型有误，请核对后重新上传
      </el-descriptions-item>
    </el-descriptions>
  </div>
  <div v-else><h1 class="nores">暂无检测结果</h1></div>
</template>

<style>
 .nores {
   text-align: center;
   color: #00bd7e;
 }
</style>

<script setup>
  import axios from "axios";
  import {ref, onMounted, defineEmits, defineProps} from 'vue'

  const emit = defineEmits(["getRecord"])


  const props = defineProps(['isupstate'])

  const color = {
    [0]: "舌色：淡白舌，比正常舌色浅淡。主气血两虚、阳虚；",
    [1]: "舌色：淡红舌，舌色淡红润泽。常见于健康人；",
    [2]: "舌色：红舌，比正常舌色红，一般有主热证；",
    [3]: "舌色：绛舌，较红舌颜色更深，或略带暗红色。主热盛证；",
    [4]: "舌色：青紫舌，可能是气虚无力推动血液运行；",
  }
  const outcolor = {
    [0]: "舌苔颜色：白苔，可能是外感风邪或体内有寒湿；",
    [1]: "舌苔颜色：黄苔，可能为实热证、虚热证或外感风热之邪；",
    [2]: "舌苔颜色：灰黑苔，可能为实热证或实寒证，寒热证程度深；",
  }
  const rot = {
    [0]: "舌苔腻，多属阳气被阴邪所遏，为寒湿夹痰或为湿热夹痰；",
    [1]: "舌苔腐，腐苔多为阳热有余；",
  }
  const thick = {
    [0]: "舌头薄，正常一般与最近饮食有关，无大碍。",
    [1]: "舌头厚，正常一般与最近饮食有关，无大碍。",
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
  let rec = ref([0]);
  let isEmpty = ref(false)

  //不做轮询，在onmountED就先get一遍record
  onMounted(function () {
      axios.get("/user/record", {
        headers:{
          'Authorization':'Bearer ' + localStorage.getItem('token')
        }
      }).then(res=> {
        rec.value = res.data.data
        console.log(rec.value)
          if(Object.keys(rec.value).length !== 0) {
            console.log('rec is not null')
            isEmpty.value = true
            reverseArray1(rec.value)
          }
      }).catch(error=> {
          console.log(error);
        })
  })

  onMounted(function () {
      const timer = window.setInterval(() => {
        setTimeout(function () {
          console.log(("开始轮询"))
          console.log(props.isupstate)
          if (props.isupstate === true || rec.value[0].state === 0) {
            console.log(("开始轮询加上向后端发送请求"))
            axios.get("/user/record", {
              headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
              }
            })
                .then(function (res) {
                  console.log(res.data)
                  rec.value = res.data.data
                  reverseArray1(rec.value)
                  console.log(rec.value)
                  console.log(rec.value[0].state)
                  if (Object.keys(rec.value).length !== 0) {
                    console.log('rec is not null')
                    isEmpty.value = true
                  }
                })
                .catch(function (error) {
                  console.log(error);
                })
                .then(res => {
                  //视情况而定
                  if (rec.value[0].state !== 0 || rec.value === []) {
                    // 这里可以写一些中止轮询的条件 比如code值返回0时
                    console.log("轮询停止")
                    emit("getRecord", false)
                    // clearInterval(timer)
                  }
                })
          }
        }, 0)
      }, 2000)
  });


</script>
