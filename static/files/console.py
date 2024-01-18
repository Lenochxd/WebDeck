import requests
import socket
import json
import time

with open('config.json', encoding="utf-8") as f:
    config = json.load(f)

def send_data(message):
    url = f"http://{socket.gethostbyname(socket.gethostname())}:{config['url']['port']}/send-data"

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'message': message
    }

    start_time = time.time()

    response = requests.post(url, headers=headers, json=data)

    end_time = time.time()
    execution_time = end_time - start_time

    if response.status_code == 200:
        print(f'success! {execution_time:.2f}s')
    else:
        print('Error:', response.status_code)

while True:
    send_data(input('Message: '))
