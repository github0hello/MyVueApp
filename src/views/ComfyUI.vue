<template>
  <div>
    <el-button @click="start_ComfyUI()">启动ComfyUI</el-button>
  </div>
  <div>
    <pre>{{ logs }}</pre>
  </div>
</template>

<script setup>
import Cookies from 'js-cookie'
import axios from 'axios'
import { ref } from 'vue'

const logs = ref('')
const start_ComfyUI = () => {
  let root_url = Cookies.get('root_url')
  if (!root_url) {
    root_url = prompt("请输入Server1的IP地址", "http://127.0.0.1:8080/")
    Cookies.set("root_url", root_url, { expires: 7 })
  }
  axios.get(`${root_url}/comfyui`)
    .then(response => {
      logs.value = response.data
      const get_logs = setInterval(() => {
        axios.get(`${root_url}/comfyui/log`)
          .then(response => {
            if (response.data === "Process Finished"){
              setTimeout(() => {
                clearInterval(get_logs)
              }, 5000);
            };
            logs.value = response.data
          })
      }, 1000);
    })
    .catch(error => {
      console.error(error)
    })
}

</script>

<style scoped>
/* 添加一些样式 */
</style>
