<template>
  <span>安装ComfyUI</span>
  <el-divider content-position="left">配置安装</el-divider>
  <el-form :model="form" ref="formRef" :rules="rules" v-if="!install_start">
    <!-- 安装路径 -->
    <el-form-item label="安装路径" prop="install_path">
      <el-input v-model="form.install_path" placeholder="/hy-tmp" />
    </el-form-item>
    <!-- ComfyUI安装源 -->
    <el-form-item label="ComfyUI安装源" prop="comfyui_mirror">
      <el-select v-model="form.comfyui_mirror" placeholder="选择ComfyUI安装源">
        <el-option label="Github" value="https://github.com/comfyanonymous/ComfyUI.git" />
        <el-option label="Gitcode" value="https://gitcode.com/gh_mirrors/co/ComfyUI.git" />
      </el-select>
    </el-form-item>
    <!-- PIP安装源 -->
    <el-form-item label="PIP安装源" prop="pip_mirror">
      <el-select v-model="form.pip_mirror" placeholder="选择PIP安装源">
        <el-option label="Pypi" value="https://pypi.org/simple" />
        <el-option label="清华源" value="https://pypi.tuna.tsinghua.edu.cn/simple" />
      </el-select>
    </el-form-item>
    <el-form-item label="是否安装ComfyUI-Manager">
      <el-switch v-model="form.install_manager" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit_config">开始安装</el-button>
    </el-form-item>
  </el-form>
  <el-steps :active="install_step" finish-status="success" v-if="install_start" direction="vertical">
    <el-step title="切换目录" />
    <el-step title="下载ComfyUI" />
    <el-step title="切换目录" />
    <el-step title="安装依赖" />
    <el-step title="安装完成" />
  </el-steps>

</template>

<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus'
import io from "socket.io-client";

const socket = io("http://127.0.0.1:8080");
const install_start = ref(false);
const formRef = ref(null);
const form = reactive({
  install_path: '/hy-tmp',
  comfyui_mirror: '',
  pip_mirror: '',
  install_manager: false,
});

const rules = {
  install_path: [
    { required: true, message: '请输入安装路径', trigger: 'blur' },
  ],
  comfyui_mirror: [
    { required: true, message: '请选择ComfyUI安装源', trigger: 'change' },
  ],
  pip_mirror: [
    { required: true, message: '请选择PIP安装源', trigger: 'change' },
  ],
};

const submit_config = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      axios.post('http://127.0.0.1:8080/api/install_comfyui', form)
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.error('安装失败:', error);
          ElMessage.error('安装失败，请检查网络或服务器状态！');
        });
    } else {
     ElMessage.error('请填写所有必填项！');
    }
  });
  install_start.value = false;
};

const installing = () => {
  socket.on("get_install_status")
}
</script>
