from flask import *
from flask_cors import CORS
import os
import json
import subprocess
from flask_socketio import SocketIO, emit
import threading
from jinja2 import Template




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


def read_config():
    with open("config.json", "r", encoding="utf-8") as f:
        config_json = json.load(f)
    hosts = config_json["ComfyUI"]["hosts"]
    device = config_json["ComfyUI"]["device"]
    cwd = config_json["ComfyUI"]["cwd"]
    port = str(config_json["ComfyUI"]["port"])
    return hosts, device, cwd, port


def run_test_bat():
    global current_process
    hosts, device, cwd, port = read_config()
    if device == "cpu":
        device_command = "--cpu"
    else:
        device_command = "--cuda"
    command = [
        r".\python_embeded\python.exe",
        "-s",
        r"ComfyUI\main.py",
        "{}".format(device_command),
        "--listen",
        hosts,
        "--port",
        port
    ]
    """运行 test.bat 并将输出实时发送到前端"""
    current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True, cwd="C:\\Users\\Administrator\\Desktop\\ComfyUI")
    for line in iter(current_process.stdout.readline, ''):
        socketio.emit('log', {'message': line.strip()})  # 发送日志到前端
    if current_process is  None:
        print("Script finished.")
    else:
        current_process.stdout.close()
        current_process.wait()
    current_process = None  # 清理进程引用
    print("Script stopped.")

@socketio.on('start_comfyui')
def handle_start_test():
    
    print("Start ComfyUI")
    if current_process is None:
        threading.Thread(target=run_test_bat).start()
    else:
        emit('log', {'message': "脚本已经在运行！"})

@socketio.on('stop_comfyui')
def handle_stop_test():
    global current_process
    if current_process:
        current_process.terminate()  # 终止子进程
        print("Stop ComfyUI")
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
tmp_status = "No Process"
@app.route('/hy-tmp/upload', methods=['GET'])
def hy_tmp_upload():
    global tmp_upload
    if tmp_status not in ["Uploading", "No Process", "Downloading"]:
        if tmp_upload.poll() is not None:
            tmp_upload = "No Process"
            tmp_status = "No Process"
            return "No Process"
    if tmp_upload == "No Process":
        with open("logs/tmp.log", "w") as log:
            tmp_upload = subprocess.Popen(['sh', 'tools/tmp.sh', "upload"], stdout=log, stderr=log)
            tmp_status = "Uploading"
            return "Start Upload"
    elif tmp_status == "Uploading":
        return "Uploading"
    else:
        app.logger.error("ERROR: ${tmp_status}")
        return "ERROR", 405
    
@app.route('/hy-tmp/download', methods=['GET'])
def hy_tmp_download():
    # 声明全局变量 tmp_upload 和 tmp_status
    global tmp_upload, tmp_status
    # 检查 tmp_status 是否不在 ["Uploading", "No Process", "Downloading"] 列表中
    if tmp_status not in ["Uploading", "No Process", "Downloading"]:
        if tmp_upload.poll() is not None:
            tmp_upload = "No Process"
            tmp_status = "No Process"
            return "No Process"
    if tmp_upload == "No Process":
        with open("logs/tmp.log", "w") as log:
            tmp_upload = subprocess.Popen(['sh', 'tools/tmp.sh', "download"], stdout=log, stderr=log)
            tmp_status = "Downloading"
            return "Start Download"
    elif tmp_status == "Downloading":
        return "Downloading"
    else:
        app.logger.error("ERROR: ${tmp_status}")
        return "ERROR", 405
    
    

# ssh -f -N -T -R 8188:localhost:8188 用户名@本地主机IP



def run_command_install(commands):
    todo_list = ["Change dir", "Clone project", "Change dir", "Install requirements"]
    global status
    for command, todo in zip(commands.split("\n"), todo_list):
        process = subprocess.run(command.split())
        if process.returncode != 0:
            status = "ERROR: " + todo
        status = todo
    status = "Finished"

@app.route('/api/install_comfyui', methods=['GET','POST'])
def install_comfyui():
    global status
    status = "No Process"
    if request.method == 'GET':
        return status
    
    print(open("tools/Templates/install", "r").read())
    cmd = Template(open("tools/Templates/install", "r").read())
    command = cmd.render(install_path=request.json['install_path'])
    threading.Thread(target=run_command_install, args=(command,)).start()
    return status

@socketio.on('get_install_status')
def get_install_status():
    global status
    socketio.emit('install_status', status)
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)

# C:\Users\Administrator\Desktop\ComfyUI
