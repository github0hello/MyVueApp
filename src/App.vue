<template>
  <el-config-provider :locale="locale"> <!-- 通过配置全局的国际化配置 -->
    <el-card style="max-width: 480px">
    <template #header>
      <div class="card-header">
        <span>Server1</span>
      </div>
    </template>
    <el-cascader v-model="value" :options="options" @change="chosseHandle" />
    <template #footer>
      <el-button type="primary" @click="OnSubmit">OK</el-button>
    </template>
  </el-card>
  </el-config-provider>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import { reactive } from 'vue'
import { computed, ref } from 'vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import axios from 'axios'

// 请求数据
const options = ref([])
axios.get('http://127.0.0.1:8080/')
  .then(function (response) {
    options.value = Array.from(response.data)
  });
const locale = computed(() => (zhCn))
const Server1_path = ref('')

const value = ref([])
const props = {
  expandTrigger: 'hover'
}

const chosseHandle = (value) => {
  Server1_path.value = value
}


const OnSubmit = () => {
  axios({
    url: 'http://127.0.0.1:5000/api',
    method: 'post',
    data: { "Server1": Server1_path.value },
  })
    .then(function (response) {
      console.log(response)
    });
}

</script>


<!-- <style scoped>
/* None */
</style> -->
