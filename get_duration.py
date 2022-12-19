import requests
import json
from datetime import datetime
from kubernetes import client, config
from concurrent.futures import ProcessPoolExecutor
import os

def get_metrics(data, limit, svc):
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

    slack_webhook(name_duration, svc)

def main():
    # get current time
    now = datetime.now()

    # interval ms
    interval = 3600000

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

        # get jaeger jason
        r = requests.get(URL)
        data = r.json()

        get_metrics(data, limit, svc_ns)

if __name__ == "__main__":
    main()