import requests
import json
from datetime import datetime
import os

def slack_webhook(svc, name, rate):
    # slack webhook
    webhook_url = os.environ['SLACK_WEBHOOK']
    channel = "#general"
    username = "Sock-shop-Alert"

    text = (f"serviecName: {svc}, memory_rate: {round(rate, 1)}%\noperationName: {name}\n3000 ms!\n{datetime.now()}")
    webhook_data = { "channel": channel, "username": username, "text": text, "icon_emoji": ":ghost:" }
    print(webhook_data.items())
    requests.post(webhook_url, data=json.dumps(webhook_data))