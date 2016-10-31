from flask import Flask
from flask import request
app = Flask(__name__)

BAD_REQUEST = 'Bad Request'
KEY_NOT_FOUND = 'Key Not Found'
OK = 'Okay'

db = {}
INSTRUCTIONS = """
Welcome to KV server. To use:
Visit endpoints to interact with store:
/set?key=5&value=2

to set 5 to 2

/get?key=5

to retrieve key for 5

All types are strings
"""


@app.route('/')
def index():
    return INSTRUCTIONS, 200


@app.route('/set', methods=['GET', 'POST'])
def set():
    try:
        key = request.args['key']
        value = request.args['value']
        db[key] = value
    except:
        return BAD_REQUEST, 400
    return OK, 200


@app.route('/get', methods=['GET', 'POST'])
def get():
    try:
        key = request.args['key']
    except:
        return BAD_REQUEST, 400

    value = db.get(key)
    if value:
        return value, 200
    return KEY_NOT_FOUND, 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
