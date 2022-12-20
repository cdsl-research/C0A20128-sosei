from prometheus_api_client import PrometheusConnect

def get_rate(svc):  
    prom = PrometheusConnect(url ="http://localhost:9090")
    
    if (svc == "front-end"):
        svc = '\"' + svc + '\"'

        memory_usage_name = "container_memory_usage_bytes{container=" + svc + "}"
        memory_limit_name = "container_spec_memory_limit_bytes{container=" + svc + "}"

        memory_usage_data = prom.get_metric_range_data(metric_name=memory_usage_name)
        memory_limit_data = prom.get_metric_range_data(metric_name=memory_limit_name)
        
        memory_usage = memory_usage_data[0].get('values')[-1][1]
        memory_limit = memory_limit_data[0].get('values')[-1][1]

        rate = 100 * (int(memory_usage) / int(memory_limit))
        
        return rate
    
    