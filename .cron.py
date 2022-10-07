# python file that gets run every so often by our cron job
import requests

host = "10.0.2.4"


res = requests.get(host+"/commands")
print(res)