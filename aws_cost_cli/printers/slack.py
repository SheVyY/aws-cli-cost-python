import json
import requests

def send_cost_to_slack(cost_data, webhook_url):
    # Convert cost data to a Slack-friendly message format
    message = "AWS Cost Data:\n"
    for service, costs in cost_data.items():
        for date, amount in costs.items():
            message += f"{service} on {date}: ${amount:.2f}\n"
    
    payload = {
        "text": message
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
