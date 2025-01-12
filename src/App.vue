<template>
  <el-config-provider :locale="locale"> <!-- 通过配置全局的国际化配置 -->
  <el-drawer
    v-model="table"
    title="I have a nested table inside!"
    direction="rtl"
    size="50%"
  >

  <el-tree style="max-width: 600px" :data="file_tree_data" show-checkbox @check-change="TreeChange"/>
  </el-drawer>

    <el-card>
      <template #header>
        <div class="card-header">
          <el-badge value="测试功能" class="item" type="primary">
            <span>目录树</span>
          </el-badge>
        </div>
      </template>
      <el-button text @click="table = true" type="primary">打开目录树</el-button>
    </el-card>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Server1</span>
        </div>
      </template>
      <el-cascader v-model="value" :options="file_tree_data" @change="chosseHandle" />
      <template #footer>
        <el-button type="primary" @click="chosses_finish">OK</el-button>
      </template>
    </el-card>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>上传到OSS</span>
        </div>
      </template>
      <el-button type="primary" @click="Uploadhytmp">Hy-Tmp</el-button>
      <el-button type="primary" @click="Uploadroot">Root</el-button>
    </el-card>
  </el-config-provider>
</template>

<script setup>
import { computed, ref } from 'vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import axios from 'axios'
import { h } from 'vue'
import { ElNotification } from 'element-plus'
import { ElLoading } from 'element-plus'

import 'element-plus/dist/index.css'

// 初始变量
const file_file_tree = ref(false) // 文件树打开状态
const root_url = prompt("请输入Server1的IP地址", "http://127.0.0.1:8080/")
const file_tree_data = ref([]) // 文件数
const locale = computed(() => (zhCn))
const Server1_path = ref('')
const value = ref([])
const table = ref(false)

// 请求文件数据
const init_loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })  //创建一个加载
axios.get(root_url)
  .then(function (response) {
    file_tree_data.value = Array.from(response.data)
    init_loading.close()
  });


const chosseHandle = (value) => {
  Server1_path.value = value
}


const chosses_finish = () => {
  axios({
    url: root_url + 'api',
    method: 'post',
    data: { "Server1": Server1_path.value },
  })
    .then(function (response) {
      console.log(response)
    });
}

// Uploadhytmp和Uploadroot是上传到OSS的响应
const Uploadhytmp = () => {
  axios.get(root_url + 'hy-tmp')
    .then(function (response) {
      ElNotification({
        title: 'Title',
        message: h('i', { style: 'color: teal' }, response.data),
      })
    });
}

const Uploadroot = () => {
  ElNotification(
    {
      title: 'sss',
      message: ''
    }
  )
}

import { ElDrawer } from 'element-plus'


const TreeChange = (data) => {
  console.log(data.value)
}

</script>


<!-- <style scoped>
/* None */
</style> -->
