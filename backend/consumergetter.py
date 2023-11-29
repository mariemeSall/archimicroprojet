import requests

def consume_messages(api_url, topic):
    response = requests.get(api_url, json=topic)
    
    if response.status_code == 200:
        print(f'Message consumed')
    else:
        print(f'Failed to consume messages')


if __name__ == '__main__':
    api_url = 'http://localhost:8000/consume'  # Replace with your FastAPI server's address
    bootstrap_servers = 'localhost:9092' # kafka's broker address
    topic = {'topic': 'coordinates'}
    consume_messages(api_url, topic)

