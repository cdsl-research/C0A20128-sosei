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
    svc = '\"' + svc + '\"'
    metrics = "container_memory_usage_bytes{container=" + svc + "}"
    metric_data = prom.get_metric_range_data(metric_name=metrics)

    t = metric_data[0].get('values')[-1][0]
    v = metric_data[0].get('values')[-1][1]
    print(datetime.datetime.fromtimestamp(t))
    print(svc)
    print(int(v) / (1000 * 1000))