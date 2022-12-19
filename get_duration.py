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

