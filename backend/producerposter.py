import requests
import random
import time

def generate_coordinate():
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    return f'{lat}; {lon}; {current_date}'

def produce_messages(api_url, bootstrap_servers, topic, num_messages):
    for _ in range(num_messages):
        message = generate_coordinate()
        payload = {'topic': topic, 'message': message, 'bootstrap_servers': bootstrap_servers}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            print(f'Message delivered: {message}')
        else:
            print(f'Failed to deliver message: {message}')

if __name__ == '__main__':
    api_url = 'http://localhost:8000/produce'  # Replace with your FastAPI server's address
    bootstrap_servers = 'localhost:9092' # kafka's broker address
    topic = 'coordinates'
    num_messages = 10
    produce_messages(api_url, bootstrap_servers, topic, num_messages)
