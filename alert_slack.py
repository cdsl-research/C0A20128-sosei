import requests
import json
from datetime import datetime
from kubernetes import client, config
from concurrent.futures import ProcessPoolExecutor
import os

def slack_webhook(metrics_dict, svc):
    # slack webhook
    webhook_url = os.environ['SLACK_WEBHOOK']
    channel = "#general"
    username = "Sock-shop-Alert"

    # μs
    duration_lim = 3000000

    # average duration for each operationName
    for key in metrics_dict:
        ave = sum(metrics_dict[key]) / len(metrics_dict[key])
        if ave >= duration_lim:
            text = f"serviecName:{svc}\noperationName:{key}\nexceed 3000 ms!\n{datetime.now()}"
            webhook_data = { "channel": channel, "username": username, "text": text, "icon_emoji": ":ghost:" }
            print(webhook_data.items())
            requests.post(webhook_url, data=json.dumps(webhook_data))