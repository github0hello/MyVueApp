from flask import *
from flask_cors import CORS
import os
import json
import subprocess
import requests
from flask_socketio import SocketIO, emit
import threading


DEBUG = True
root_dir = "C:\\Users\\Administrator\\Desktop\\ComfyUI\\ComfyUI"
if not DEBUG:
    os.system("oss login")
    root_dir = "/hy-tmp/"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 用于存储当前运行的子进程
current_process = None


def run_test_bat():
    global current_process
    command = [
        r".\python_embeded\python.exe",
        "-s",
        r"ComfyUI\main.py",
        "--cpu",
        "--windows-standalone-build",
        "--listen",
        "0.0.0.0"
    ]
    """运行 test.bat 并将输出实时发送到前端"""
    current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True, cwd="C:\\Users\\Administrator\\Desktop\\ComfyUI")
    for line in iter(current_process.stdout.readline, ''):
        socketio.emit('log', {'message': line.strip()})  # 发送日志到前端
    current_process.stdout.close()
    current_process.wait()
    current_process = None  # 清理进程引用

@socketio.on('start_test')
def handle_start_test():
    
    print("Start ComfyUI")
    if current_process is None:
        threading.Thread(target=run_test_bat).start()
    else:
        emit('log', {'message': "脚本已经在运行！"})

@socketio.on('stop_test')
def handle_stop_test():
    print("Stop ComfyUI")
    global current_process
    if current_process:
        current_process.terminate()  # 终止子进程
        current_process = None
        emit('log', {'message': "脚本已停止。"})
    else:
        emit('log', {'message': "没有正在运行的脚本。"})









def get_dir_tree_json(root_dir):
    """
    获取目录树结构
    """
    def get_dir_tree(root_dir):
        dir_tree = []
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            if os.path.isdir(item_path):
                children = get_dir_tree(item_path)
                dir_tree.append({
                    'value': root_dir + item,
                    'label': item,
                    'children': children
                })
            else:
                dir_tree.append({
                    'value': root_dir + item,
                    'label': item
                })
        return dir_tree

    if not os.path.exists(root_dir) or not os.path.isdir(root_dir):
        return "输入的路径不存在或不是文件夹", 500

    dir_tree = get_dir_tree(root_dir)
    return json.dumps(dir_tree, ensure_ascii=False, indent=2)



@app.route('/')
def index():
    try:
        dir_tree_json = get_dir_tree_json(root_dir)
        return dir_tree_json
    except ValueError as e:
        print(e)
        return str(e)


@app.route('/api', methods=['GET','POST'])
def api():
    # 获取请求的Path
    path = str()
    for i in request.json['Server1']:
        path = path + i + "\\"
    print(root_dir + path)
    return "OK"

tmp_upload = "No Process"
@app.route('/hy-tmp', methods=['GET'])
def hy_tmp():
    if not DEBUG:
        global tmp_upload
        if tmp_upload != "No Process":
            if tmp_upload.poll() is not None:
                tmp_upload = "No Process"
                return "Process Finished"
            return "Process Running"
        with open("logs/tmp.log", "w") as log:
            tmp_upload = subprocess.Popen(['sh', 'tools/tmp.sh'], stdout=log, stderr=log)
    return "OK"


comfyui_process = "No Process"
@app.route("/comfyui")
def comfyui():
    global comfyui_process
    if comfyui_process != "No Process":
        if comfyui_process.poll() is not None:
            comfyui_process = "No Process"
    if comfyui_process != "No Process":
        return "Process Running"
    with open("logs/comfyui.log", "w") as log:
        comfyui_process = subprocess.Popen(['bash', 'tools/comfyui.sh'], stdout=log)
    return "OK"

@app.route("/comfyui/log")
def comfyui_log():
    global comfyui_process
    if comfyui_process != "No Process":
        if comfyui_process.poll() is not None:
            comfyui_process = "No Process"
            return "Process Finished"
    else:
        return "Process Finished"
    with open("logs/comfyui.log", "r") as log:
        return log.read()

# ssh -f -N -T -R 8188:localhost:8188 用户名@本地主机IP


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)

# C:\Users\Administrator\Desktop\ComfyUI
