from flask import Flask
from flask import request

from database.db import db


app = Flask(__name__)

BAD_REQUEST = 'Bad Request'
KEY_NOT_FOUND = 'Key Not Found'
OK = 'Okay'

INSTRUCTIONS = """
Welcome to KV server.
"""


@app.route('/')
def index():
    return INSTRUCTIONS, 200


@app.route('/set', methods=['GET', 'POST'])
def set():
    try:
        data = request.get_json()
        for k, v in data.items():
            db.put(k, v)
    except:
        return BAD_REQUEST, 400
    return OK, 200


@app.route('/get', methods=['GET', 'POST'])
def get():
    try:
        key = request.get_json()
        value = db.get(key)
    except:
        return BAD_REQUEST, 400

    if value:
        return value, 200
    return KEY_NOT_FOUND, 404


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    try:
        keys = request.get_json()
        for key in keys:
            db.delete(key)
        return OK, 200
    except:
        return BAD_REQUEST, 400


if __name__ == "__main__":
    app.run(host='0.0.0.0')
