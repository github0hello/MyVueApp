from flask import Flask, request
from flask_cors import CORS
import os
import json
import subprocess
DEBUG = True
root_dir = "C:\\Users\\Administrator\\Desktop\\ComfyUI"
if not DEBUG:
    os.system("oss login")
    root_dir = "/hy-tmp/"
app = Flask(__name__)
CORS(app)
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
        raise ValueError("输入的路径不存在或不是文件夹")

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

@app.route('/hy-tmp', methods=['GET'])
def hy_tmp():
    if not DEBUG:
        result = subprocess.run(['sh', 'tools/tmp.sh'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr)
        return result.stdout
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
app.run(debug=True, port=8080, host="0.0.0.0")

# C:\Users\Administrator\Desktop\ComfyUI
