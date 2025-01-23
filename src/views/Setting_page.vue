<template>
  <h1>设置</h1>
  <el-divider content-position="left">服务器URL</el-divider>
  <el-input
      v-model="root_url"
      placeholder="127.0.0.1:8080"
    >
      <template #prepend>http://</template>
      <template #append>
    <el-button @click="reset_root_url">重置</el-button>
  </template>
    </el-input>

</template>


<script setup>
import { ref } from 'vue'
import Cookies from 'js-cookie'
const root_url = ref('')

const reset_root_url = () => {
  const response = fetch(root_url.value, { method: 'HEAD' })
  console.log(response)
  Cookies.set("root_url", "http://"+root_url.value, { expires: 7 })
  window.location.href = window.location.href

}

</script>
