from flask import Flask, request
from flask_cors import CORS
import os
import json
import subprocess
DEBUG = True
root_dir = "C:\Users\Administrator\Desktop\ComfyUI"
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
        # 指定 Shell 脚本的路径
        script_path = '/hy-tmp/tmp.sh'
        
        # 运行 Shell 脚本
        result = subprocess.run(['sh', script_path], capture_output=True, text=True)
        
        # 检查子进程的返回码
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr)
                # 压缩hy-tmp文件夹
        return result.stdout
    return "OK"
app.run(debug=DEBUG, port=8080, host="0.0.0.0")

# C:\Users\Administrator\Desktop\ComfyUI
