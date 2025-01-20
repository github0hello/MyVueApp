<template>
  <h1>设置</h1>
  <el-divider content-position="left">服务器URL</el-divider>
  <el-input
      v-model="input1"
      placeholder="127.0.0.1:8080"
    >
      <template #prepend>http://</template>
    </el-input>
</template>


<script setup>

</script>
