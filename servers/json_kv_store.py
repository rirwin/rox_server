from flask import Flask
from flask import request
import simplejson

app = Flask(__name__)


#import ipdb;ipdb.set_trace()
#db = {}
INSTRUCTIONS = """
Welcome to KV server. To use:
Visit endpoints to interact with store:
/set?key=5&value={"k": "v"}

to set 5 to 2

/get?key=5

to retrieve key for 5
"""


@app.route('/')
def index():
    return INSTRUCTIONS, 200


@app.route('/set', methods=['GET', 'POST'])
def set():
    try:
        key = request.args['key']
        raw_value = request.args['value']
        db[key] = simplejson.loads(raw_value)
    except:
        return 'Bad Request', 400
    return 'OK', 200


@app.route('/get', methods=['GET', 'POST'])
def get():
    try:
        key = request.args['key']
    except:
        return 'Bad Request', 400

    value = db.get(key)
    if value:
        return simplejson.dumps(value), 200
    return 'Key Not Found', 404


if __name__ == "__main__":
    db = {}
    app.run(debug=True)
