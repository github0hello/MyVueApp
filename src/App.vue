<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">
        <!-- 导航 -->
        <el-menu default-active="1" class="el-menu-vertical-demo">
          <el-menu-item index="1" @click="$router.push('/')">
            <!-- 储存管理 -->
            <el-icon>
              <location />
            </el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span>功能</span>
            </template>
            <el-menu-item-group title="ComfyUI">
              <el-menu-item index="1-1">安装</el-menu-item>
              <el-menu-item index="1-2">启动</el-menu-item>
            </el-menu-item-group>

          </el-sub-menu>


          <el-menu-item index="3" @click="$router.push('/settings')">
            <!-- 设置 -->
            <el-icon>
              <setting />
            </el-icon>
            <span>设置</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <RouterView />
        </el-main>
      </el-container>
    </el-container>
  </div>




</template>

<script setup>
import {
  Location,
  Setting,
} from '@element-plus/icons-vue'


</script>
