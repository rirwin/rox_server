from flask import Flask
from flask import request
import simplejson

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


@app.route('/add', methods=['GET', 'POST'])
def add():
    try:
        data = request.get_json()
        if not data:
            raise Exception
        db.add_to_row(data)
    except:
        return BAD_REQUEST, 400
    return OK, 200


@app.route('/set', methods=['GET', 'POST'])
def set():
    try:
        data = request.get_json()
        if not data:
            raise Exception
        db.set(data)
    except:
        return BAD_REQUEST, 400
    return OK, 200


@app.route('/get', methods=['GET', 'POST'])
def get():
    try:
        keys = request.get_json()
        if not keys:
            raise Exception
        data = db.get(keys)
    except:
        return BAD_REQUEST, 400

    return simplejson.dumps(data), 200


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    try:
        keys = request.get_json()
        if not keys:
            raise Exception
        db.delete(keys)
        return OK, 200
    except:
        return BAD_REQUEST, 400


if __name__ == "__main__":
    app.run(host='0.0.0.0')
