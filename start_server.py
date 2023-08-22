from flask import Flask
import json
import socket

app = Flask(__name__)

with open('config.json', encoding= "utf-8") as f:
    config = json.load(f)
        
@app.route('/61432/webdeck/start', methods=['POST'])
def main():
    print(config['url']['ip']+':'+config['url']['port'])
    return str(socket.gethostbyname(socket.gethostname()),':',config['url']['port'])

if __name__ == '__main__':
    print('start_server started')
    app.run(host='0.0.0.0', port=61432, debug=False)