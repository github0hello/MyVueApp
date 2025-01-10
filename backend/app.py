from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api', methods=['GET','POST'])
def api():
    print(request.json)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)