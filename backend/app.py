from flask import Flask
from flask import request
from flask_cors import CORS
import urllib.request


app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET','POST'])
def api():
    print(request.json)
    return "OK"

if __name__ == '__main__':
    print(" * 检查链接")
    try:
        urls = ["http://127.0.0.1:8080/"]
        for url in urls:
            status = urllib.request.urlopen(url).code
            if status == 200:
                print(" * 链接正常")
    except Exception as err:
        print(err)
        print(" * 链接失败")
        exit(1)
    app.run(debug=True)