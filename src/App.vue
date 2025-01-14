<template>


  <el-config-provider :locale="locale"> <!-- 通过配置全局的国际化配置 -->
  <!-- 目录树 -->
    <el-drawer v-model="file_tree_state" title="I have a nested table inside!" direction="rtl" size="50%">

      <el-tree style="max-width: 600px" :data="file_tree_data" show-checkbox @check-change="TreeChange" />
      <el-button type="primary" @click="chosses_tree_finish">OK</el-button>
    </el-drawer>
    <el-card>
      <template #header>
        <div class="card-header">
          <el-badge value="测试功能" class="item" type="primary">
            <span>目录树</span>
          </el-badge>
        </div>
      </template>
      <el-button text @click="file_tree_state = true" type="primary">打开目录树</el-button>
    </el-card>
    <!-- 选择模块 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Server1</span>
          <button class="reset_button" @click="reset_root_url">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="20" height="20">
              <path fill="currentColor"
                d="M784.512 230.272v-50.56a32 32 0 1 1 64 0v149.056a32 32 0 0 1-32 32H667.52a32 32 0 1 1 0-64h92.992A320 320 0 1 0 524.8 833.152a320 320 0 0 0 320-320h64a384 384 0 0 1-384 384 384 384 0 0 1-384-384 384 384 0 0 1 643.712-282.88z">
              </path>
            </svg>
          </button>
          <br>
          <span>IP: {{ root_url }}</span>
        </div>
      </template>
      <el-cascader v-model="value" :options="file_tree_data" @change="chosseHandle" />
      <template #footer>
        <el-button type="primary" @click="chosses_finish">OK</el-button>
      </template>
    </el-card>
    <!-- 上传到OSS -->
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
import { computed, ref, h } from 'vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import axios from 'axios'
import { ElNotification, ElLoading , ElMessage} from 'element-plus'
import Cookies from 'js-cookie'
import 'element-plus/dist/index.css'




// 初始变量
const file_tree_state = ref(false) // 文件树打开状态
let root_url = "" // Server1的IP地址
const file_tree_data = ref([]) // 文件数
const locale = computed(() => (zhCn))
const Server1_path = ref('')
const value = ref([])
let chosse_file = []




// 使用Cookie存储Root_url
// this.$cookies.set("root_url", root_url)

// 获取url
if (Cookies.get("root_url") == null) {
  root_url = prompt("请输入Server1的IP地址", "http://127.0.0.1:8080/")
  Cookies.set("root_url", root_url, { expires: 7 })
} else {
  root_url = Cookies.get("root_url")
}

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
  })
  .catch(function (error) {
    init_loading.close()
    ElMessage({
    message: error,
    type: 'error',
    plain: true,
  })
})


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



const reset_root_url = () => {
  root_url = prompt("请输入Server1的IP地址", "http://127.0.0.1:8080/")
  Cookies.set("root_url", root_url, { expires: 7 })
  window.location.href = window.location.href

}

const TreeChange = (data   ) => {
  if (chosse_file.includes(data.value)) {
  // pass
} else {
    chosse_file.push(data.value);
}
}

const chosses_tree_finish = () => {
  console.log(chosse_file)
}
</script>


<style scoped>
/* 设置重置URL按钮为透明 */
.reset_button {
  background-color: transparent;
  border: none;
  padding: 10px 20px;
  outline: none;
}
</style>
