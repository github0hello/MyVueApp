import flask
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!', [("Access-Control-Allow-Origin", "*")]

if __name__ == '__main__':
    app.run(debug=True)