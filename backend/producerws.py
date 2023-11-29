import websocket
import random
import time
import json

def generate_coordinate():
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    return {'lat': lat, 'lon': lon, 'timestamp': current_date}

def produce_messages(ws_url, num_messages):
    ws = websocket.create_connection(ws_url)

    for _ in range(num_messages):
        message = generate_coordinate()
        payload = {'topic': 'coordinates', 'message': message}
        ws.send(json.dumps(payload))

        result = ws.recv()
        print(f"Received from server: {result}")

    ws.close()

if __name__ == '__main__':
    ws_url = 'ws://localhost:8000/ws'  # Replace with your WebSocket server's address
    num_messages = 10
    produce_messages(ws_url, num_messages)
