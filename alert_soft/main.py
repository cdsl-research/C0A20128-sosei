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
    duration_lim = 500

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
        # svc_ns_list.append(i.metadata.name + "." + namespace)

    for svc in svc_list: 
        # jaeger ui url
        URL = ( "http://localhost:" + str(port)
                + "/jaeger/api/traces"
                + "?end=" + ts_end 
                + "&limit=" + str(limit)
                + "&lookback=1h&maxDuration&minDuration"
                + "&service=" + svc + "." + namespace
                + "&start="+ ts_start )

        # get jaeger jason
        r = requests.get(URL)
        data = r.json()

        duration_dict = duration.get_duration(data, limit)
        # print(duration_dict)
        for key in duration_dict:
            ave = sum(duration_dict[key]) / len(duration_dict[key])
            if ave >= duration_lim:
                memory_rate = memory.get_rate(svc)
                print(memory_rate)
                if ((memory_rate != None) and (memory_rate >= 5)):
                    alert.slack_webhook(svc, key, memory_rate)
                    print("alert!")


if __name__ == "__main__":
    main()