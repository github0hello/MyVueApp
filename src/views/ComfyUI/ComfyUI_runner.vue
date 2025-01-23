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


<style>
.terminal {
  width: 50%;
  height: 50%;
  background-color: #000;
  border: 1px solid #333;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 10%;
  left: 10%;
  resize: both;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
}

.terminal-header {
  background-color: #1e1e1e;
  color: #fff;
  padding: 10px 20px;
  border-radius: 10px 10px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: move;
  user-select: none;

}

.terminal-header .terminal-title {
  font-size: 16px;
  margin: 0;
}

.terminal-header .controls {
  display: flex;
  align-items: center;
}

.terminal-header .controls button {
  background-color: transparent;
  border: none;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  margin-left: 10px;
}

.terminal-header .controls button:hover {
  text-shadow: 0 0 2px #fff;
}

.terminal-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  font-size: 14px;
  overflow:auto;
  height: calc(100% - 40px);

}

.terminal-content p {
  margin: 5px 0;
  color: #fff;
}

.terminal-content .error {
  color: #f00;
}

.terminal-content .warning {
  color: #ff0;
}

.terminal-content .info {
  color: #0ff;
}

.start-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reopen-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #333;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

/* 浮动按钮样式 */
.floating-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

/* From Deepseek */
.terminal-content::-webkit-scrollbar {
  width: 8px;
}

.terminal-content::-webkit-scrollbar-track {
  background: #1e1e1e;
}

.terminal-content::-webkit-scrollbar-thumb {
  background: #666;
  border-radius: 4px;
}

.terminal-content {
  scrollbar-width: thin; /* Firefox */
  scrollbar-color: #666 #1e1e1e; /* Firefox */
  overflow-y: auto;
}



.terminal-header {
  flex-shrink: 0; /* 防止标题栏被压缩 */
}

.terminal-content {
  flex: 1;
  min-height: 100px; /* 保证最小高度 */
}
</style>
