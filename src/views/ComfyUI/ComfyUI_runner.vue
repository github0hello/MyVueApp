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



    <!-- 浮动按钮 -->
    <button class="floating-btn" @click="toggleScript">{{ buttonLabel }}</button>
  </div>
</template>

<script>
import io from "socket.io-client";

export default {
  data() {
    return {
      currentView: "start", // 控制显示终端或启动页面
      terminalOpen: false, // 终端是否打开
      displayState: "block", // 终端显示状态
      logs: [], // 终端日志
      socket: io("http://127.0.0.1:8080"), // Socket.io 实例
      isDragging: false, // 是否正在拖动
      offsetX: 0, // 拖动偏移量
      offsetY: 0,
      isScriptRunning: false, // 脚本是否正在运行
    };
  },
  computed: {
    // 动态计算按钮文本
    buttonLabel() {
      if (!this.terminalOpen) {
        return "打开窗口";
      } else if (this.isScriptRunning) {
        return "停止脚本";
      } else {
        return "运行脚本";
      }
    },
  },
  methods: {
    // 启动脚本
    startScript() {
      this.socket.emit("start_test");
      this.isScriptRunning = true;
      this.currentView = "terminal"; // 切换到终端视图
      this.terminalOpen = true;
    },
    // 停止脚本
    stopScript() {
      this.socket.emit("stop_test");
      this.isScriptRunning = false;
    },
    // 关闭终端
    closeTerminal() {
      this.currentView = "start"; // 切换回启动页面
      this.terminalOpen = false;
      this.isScriptRunning = false;
    },
    // // 重新打开终端
    // reopenTerminal() {
    //   this.currentView = "terminal";
    //   this.terminalOpen = true;
    // },
    // 最小化终端
    minimize() {
      this.$refs.terminal.style.height = "50px";
      this.$refs.terminal.style.overflow = "hidden";
      this.$refs.terminalContent.style.display = "none";
    },
    // 切换全屏
    toggleFullScreen() {
      if (!document.fullscreenElement) {
        this.$refs.terminal.requestFullscreen().catch((err) => {
          console.error(`无法进入全屏模式: ${err.message}`);
        });
      } else {
        document.exitFullscreen().catch((err) => {
          console.error(`无法退出全屏模式: ${err.message}`);
        });
      }
    },
    // 开始拖动
    startDragging(event) {
      this.isDragging = true;
      this.offsetX = event.clientX - this.$refs.terminal.getBoundingClientRect().left;
      this.offsetY = event.clientY - this.$refs.terminal.getBoundingClientRect().top;

      document.addEventListener("mousemove", this.onDragging);
      document.addEventListener("mouseup", this.stopDragging);
    },
    // 拖动中
    onDragging(event) {
      if (this.isDragging) {
        this.$refs.terminal.style.left = `${event.clientX - this.offsetX}px`;
        this.$refs.terminal.style.top = `${event.clientY - this.offsetY}px`;
      }
    },
    // 停止拖动
    stopDragging() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDragging);
      document.removeEventListener("mouseup", this.stopDragging);
    },
    // 切换脚本运行状态
    toggleScript() {
      if (!this.terminalOpen) {
        // 如果终端未打开，打开终端
        this.reopenTerminal();
      } else if (this.isScriptRunning) {
        // 如果脚本正在运行，停止脚本
        this.stopScript();
      } else {
        // 如果脚本未运行，启动脚本
        this.startScript();
      }
    },
  },
  mounted() {
    // 监听日志消息
    this.socket.on("log", (data) => {
      console.log("Received log message:", data);
      this.logs.push(data);
      this.$nextTick(() => {
        this.$refs.terminalContent.scrollTop = this.$refs.terminalContent.scrollHeight;
      });
    });

    // 监听停止脚本消息
    this.socket.on("stop_test", () => {
      this.isScriptRunning = false;
      this.logs.push({ type: "info", message: "脚本已停止。" });
    });
  },
};
</script>

<style>
.terminal {
  width: 80%;
  height: 80%;
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
}

.terminal-content .log-message {
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
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}
</style>
