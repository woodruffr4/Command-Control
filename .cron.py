# python file that gets run every so often by our cron job
import subprocess, os, requests

host = "http://10.0.2.4:5000"


cmds = requests.get(host+"/commands").json()

print("---- Running commands -----")
for cmd in cmds:
    print("\n")
    print("root#", cmd)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode("utf-8"), error, "\n")