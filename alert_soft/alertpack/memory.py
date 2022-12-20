import datetime
from kubernetes import client, config
from prometheus_api_client import PrometheusConnect

svc_list = []
namespace = "sock-shop"
config.load_kube_config()
v1 = client.CoreV1Api()

svcs = v1.list_namespaced_service(namespace)
for i in svcs.items:
    svc_list.append(i.metadata.name)

prom = PrometheusConnect(url ="http://localhost:9090")
for svc in svc_list:
    if (svc == "front-end"):
        svc = '\"' + svc + '\"'

        memory_usage_name = "container_memory_usage_bytes{container=" + svc + "}"
        memory_limit_name = "container_spec_memory_limit_bytes{container=" + svc + "}"

        memory_usage_data = prom.get_metric_range_data(metric_name=memory_usage_name)
        memory_limit_data = prom.get_metric_range_data(metric_name=memory_limit_name)
        
        memory_usage = memory_usage_data[0].get('values')[-1][1]
        memory_limit = memory_limit_data[0].get('values')[-1][1]

        rate = str(100 * (int(memory_usage) / int(memory_limit))) + "%"

        print(svc, rate)
    
    