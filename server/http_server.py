from flask import Flask
from flask import request


try:
    import rocksdb
    db = rocksdb.DB("rox_server_kernel.db", rocksdb.Options(create_if_missing=True))  # pragma: no cover
    print("Using RocksDB")                                                            # pragma: no cover
except ImportError:
    from server.dict_database import DictDatabase
    db = DictDatabase()
    print("Using In-Memory Dictionary")


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
            db.put(str.encode(k), str.encode(v))
    except:
        return BAD_REQUEST, 400
    return OK, 200


@app.route('/get', methods=['GET', 'POST'])
def get():
    try:
        key = request.get_json()
        encoded_key = str.encode(key)
    except:
        return BAD_REQUEST, 400

    value = db.get(encoded_key)
    if value:
        return value, 200
    return KEY_NOT_FOUND, 404


@app.route('/clear_key', methods=['GET', 'POST'])
def clear_key():
    try:
        key = request.get_json()
        encoded_key = str.encode(key)
        db.delete(encoded_key)
        return OK, 200
    except:
        return BAD_REQUEST, 400


if __name__ == "__main__":
    app.run(host='0.0.0.0')
