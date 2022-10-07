# flask server to host on attackers machine
# Provides an endpoint which will return a list of commands to run on the target machine

import flask
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
cors = CORS(app)

@app.route('/commands', methods=['GET'])
@cross_origin()
def commands():
    return flask.jsonify(['ls', 'pwd', 'id'])
