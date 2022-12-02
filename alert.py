import requests
import json
from datetime import datetime
from kubernetes import client, config

# get current time
now = datetime.now()

# interval μs
interval = 600000000

# duration limit μs
duration_lim = 5000

# now(end)～$interval μs ago(start)
ts_end = str(datetime.timestamp(now)).replace('.', '')
ts_start = str(datetime.timestamp(now) - interval).replace('.', '')

# jaeger port
port = 16686

# serch limit
limit = 20

# get kubernetes svc
svc_ns_list = []
namespace = "sock-shop"
config.load_kube_config()
v1 = client.CoreV1Api()

svcs = v1.list_namespaced_service(namespace)
for i in svcs.items:
    svc_ns_list.append( i.metadata.name + "." + namespace )

for svc_ns in svc_ns_list: 
    # jaeger ui url
    URL = ( "http://localhost:" + str(port)
            + "/jaeger/api/traces"
            + "?end=" + ts_end 
            + "&limit=" + str(limit)
            + "&lookback=1h&maxDuration&minDuration"
            + "&service=" + svc_ns
            + "&start="+ ts_start )

    # slack webhook
    webhook_url = ''
    channel = "#general"
    username = "Sock-shop-Alert"

    # get jaeger jason
    r = requests.get(URL)
    data = r.json()

    # get duration for each operationName
    name_duration = {}

    for i in range(limit):
        try:
            traceID = data['data'][i]
        except IndexError: 
            print(f"Number of traceID under limit")
            break

        for j in range(len(traceID['spans'])):
            operationName = traceID['spans'][j]['operationName']
            duration = traceID['spans'][j]['duration']
            if (operationName not in name_duration ):
                name_duration[operationName] = [duration]
            else:
                name_duration[operationName].append(duration)

    # average duration for each operationName
    for key in name_duration:
        ave = sum(name_duration[key]) / len(name_duration[key])
        if ave >= duration_lim:
            text = f"serviecName:{svc_ns}\noperationName:{key}\nexceed {duration_lim}μs!"
            webhook_data = { "channel": channel, "username": username, "text": text, "icon_emoji": ":ghost:" }
            print(webhook_data.items())
            requests.post(webhook_url, data=json.dumps(webhook_data))
