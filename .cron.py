# python file that gets run every so often by our cron job
import subprocess, os, requests, sys

# pass in host as argument
host = sys.argv[1]


cmds = requests.get(host).json()

print("---- Running commands -----")
for cmd in cmds:
    print("\n")
    print("root#", cmd)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode("utf-8"), error, "\n")