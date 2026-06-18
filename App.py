from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "vibecoding"
ACCESS_TOKEN = "EAAaZCEWoBx6IBRrLLQZB2YUaGPpD1H1DzzZCkzdcsDo4ZBZCrlV4hh6TrlVnZBCf4ax8NegdDdPp19TTO2kcQnYj9iq8lCzHJwNsRXaZBfDZAjke1zzMl203WaZAZCNk7EXNg7tMlX7SANy4rD5Wtl8FnMMUUY2UYNkrtADmAYdrcJCbZArHVSQZCE8WWYTZC4gT6RHNtmw0yjowNeHZBAEjukPD66D9TwccT5ZCPuTnAZDZD"
PHONE_NUMBER_ID = "106540352242922"

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'whatsapp_business_account':
        for entry in data['entry']:
            for change in entry['changes']:
                if change['field'] == 'messages':
                    msg = change['value']['messages'][0]
                    from_number = msg['from']
                    text = msg['text']['body']
                    reply = f"سلام! تا وویل: {text}\nزه ستا AI یم، څه خدمت وکړم؟"
                    send_message(from_number, reply)
    return 'ok', 200

def send_message(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)

if __name__ == '__main__':
    app.run(port=5000)
