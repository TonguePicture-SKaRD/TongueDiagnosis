<script setup>
  import axios from "axios";

  let record = ref(0);
  async function handleClick(event){
    axios.get('http://127.0.0.1:5000/api/user/record',{
    }).then(res=>{
      console.log(res)
      console.log(res.data)
      record = res.data
    }).catch(error=>{
      console.log(error)
    })
  }
  let len = record.length
  let state = record[len].state
  const postFontSize = state
</script>
<template>
  <button @click="handleClick">215654</button>

</template>