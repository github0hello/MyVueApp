<template>
  <div>
    <!-- 终端窗口 -->
    <div v-if="currentView === 'terminal'" class="terminal" :style="{ display: displayState }" ref="terminal">
      <div class="terminal-header" @mousedown="startDragging">
        <h1 class="terminal-title">终端日志</h1>
        <div class="controls">
          <button @click="minimize">-</button>
          <button @click="toggleFullScreen">▢</button>
          <button @click="closeTerminal">x</button>
        </div>
      </div>
      <div class="terminal-content" ref="terminalContent">
        <p v-for="(log, index) in logs" :key="index" :class="log.type" class="log-message">{{ log.message }}</p>
      </div>
    </div>

    <el-button class="floating-btn" @click="toggleScript">{{ buttonLabel }}</el-button>
    <div>
      <span>ComfyUI运行状态</span>
      <br>
      <span v-if="isScriptRunning">运行中</span>
      <span v-else>未运行</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from "vue";
import io from "socket.io-client";

export default {
  setup() {
    const currentView = ref("start");
    const terminalOpen = ref(false);
    const displayState = ref("block");
    const logs = ref([]);
    const socket = io("http://127.0.0.1:8080");
    const isDragging = ref(false);
    const offsetX = ref(0);
    const offsetY = ref(0);
    const isScriptRunning = ref(false);
    const terminal = ref(null);
    const terminalContent = ref(null);

    const buttonLabel = computed(() => {
      if (!terminalOpen.value) {
        return "打开窗口";
      } else if (isScriptRunning.value) {
        return "停止脚本";
      } else {
        return "运行脚本";
      }
    });

    const startScript = () => {
      socket.emit("start_comfyui");
      isScriptRunning.value = true;
      currentView.value = "terminal";
      terminalOpen.value = true;
    };

    const stopScript = () => {
      socket.emit("stop_comfyui");
      isScriptRunning.value = false;
    };

    const closeTerminal = () => {
      currentView.value = "start";
      terminalOpen.value = false;
      isScriptRunning.value = false;
    };

    const reopenTerminal = () => {
      currentView.value = "terminal";
      terminalOpen.value = true;
    };

    const minimize = () => {
      terminal.value.style.height = "50px";
      terminal.value.style.width = "300px";
      terminal.value.style.overflow = "hidden";
      terminalContent.value.style.display = "none";
    };

    const toggleFullScreen = () => {
      if (!document.fullscreenElement) {
        terminal.value.requestFullscreen().catch((err) => {
          console.error(`无法进入全屏模式: ${err.message}`);
        });
      } else {
        document.exitFullscreen().catch((err) => {
          console.error(`无法退出全屏模式: ${err.message}`);
        });
      }
    };

    const startDragging = (event) => {
      isDragging.value = true;
      offsetX.value = event.clientX - terminal.value.getBoundingClientRect().left;
      offsetY.value = event.clientY - terminal.value.getBoundingClientRect().top;

      document.addEventListener("mousemove", onDragging);
      document.addEventListener("mouseup", stopDragging);
    };

    const onDragging = (event) => {
      if (isDragging.value) {
        terminal.value.style.left = `${event.clientX - offsetX.value}px`;
        terminal.value.style.top = `${event.clientY - offsetY.value}px`;
      }
    };

    const stopDragging = () => {
      isDragging.value = false;
      document.removeEventListener("mousemove", onDragging);
      document.removeEventListener("mouseup", stopDragging);
    };

    const toggleScript = () => {
      if (!terminalOpen.value) {
        reopenTerminal();
      } else if (isScriptRunning.value) {
        stopScript();
      } else {
        startScript();
      }
    };

    onMounted(() => {
      socket.on("log", (data) => {
        logs.value.push(data);
        terminalContent.value.scrollTop = terminalContent.value.scrollHeight;


      });

      socket.on("stop_comfyui", () => {
        isScriptRunning.value = false;
        logs.value.push({ type: "info", message: "脚本已停止。" });
      });
    });

    onUnmounted(() => {
      socket.off("log");
      socket.off("stop_comfyui");
    });

    return {
      currentView,
      terminalOpen,
      displayState,
      logs,
      terminal,
      terminalContent,
      buttonLabel,
      isScriptRunning,
      startScript,
      stopScript,
      closeTerminal,
      reopenTerminal,
      minimize,
      toggleFullScreen,
      startDragging,
      onDragging,
      stopDragging,
      toggleScript,
    };
  },
};
</script>


<style src="@/assets/ComfyUI/runner.css"> </style>
