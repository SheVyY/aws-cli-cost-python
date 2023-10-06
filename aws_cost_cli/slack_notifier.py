from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_slack_notification(token, channel, message):
    client = WebClient(token=token)
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        assert response["message"]["text"] == message
    except SlackApiError as e:
        print(f"Error sending Slack message: {e.response['error']}")
