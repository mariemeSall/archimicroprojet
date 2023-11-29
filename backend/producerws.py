import websocket
import random
import time
import json

def generate_coordinate():
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    return {'lat': lat, 'lon': lon, 'timestamp': current_date}

def produce_messages(ws_url, bootstrap_servers, topic, num_messages):
    ws = websocket.create_connection(ws_url)

    for _ in range(num_messages):
        message = generate_coordinate()
        payload = {'topic': topic, 'message': message, 'bootstrap_servers': bootstrap_servers}
        ws.send(json.dumps(payload))

        result = ws.recv()
        print(f"Received from server: {result}")

    ws.close()

if __name__ == '__main__':
    # ws_url = 'ws://localhost:8000/ws'  # Websocket URL local
    ws_url = 'ws://0.0.0.0:8000/ws'  # Websocket URL
    bootstrap_servers = 'localhost:9092' # kafka's broker address
    TOPIC = 'coordinates'
    num_messages = 10
    produce_messages(ws_url, bootstrap_servers, TOPIC, num_messages)

