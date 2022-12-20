import requests
from datetime import datetime
from kubernetes import client, config
import os
from alertpack import *

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
    svc_list = []
    svc_ns_list = []
    namespace = "sock-shop"
    config.load_kube_config()
    v1 = client.CoreV1Api()

    svcs = v1.list_namespaced_service(namespace)
    for i in svcs.items:
        svc_list.append(i.metadata.name)
        svc_ns_list.append(i.metadata.name + "." + namespace)

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

        get_duration.get_metrics(data, limit, svc_ns)

if __name__ == "__main__":
    main()