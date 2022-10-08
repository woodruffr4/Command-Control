# python file that gets run every so often by our cron job
import subprocess, requests, sys, traceback
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from base64 import b64decode

# pass in host as argument
host = sys.argv[1]
public_key_path = ".public.pem"

result = requests.get(host).json()
message = result['message']
signature = b64decode(result['signature'])

# decode commands
with open(public_key_path, 'r') as f:
    public_key = RSA.import_key(f.read())

# verify commands
try:
    hash = SHA256.new(message.encode())
    pkcs1_15.new(public_key).verify(hash, signature)
    commands = message.split("\n")
except (ValueError, TypeError):
    print("Signature verification failed")
    traceback.print_exc()
    sys.exit(1)

print("---- Running commands -----")
for cmd in commands:
    print("\n")
    print("root#", cmd)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode("utf-8"), error.decode("utf-8"), "\n")