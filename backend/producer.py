import random
import time
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def generate_coordinate():
    # Generate random latitude and longitude
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)

    # Get the current date and time in ISO format
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    return f'{lat}; {lon}; {current_date}'

def produce_messages(bootstrap_servers, topic, num_messages):
    producer_conf = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_conf)

    for _ in range(num_messages):
        message = generate_coordinate()
        producer.produce(topic, value=message, callback=delivery_report)

    producer.flush()

if __name__ == '__main__':
    bootstrap_servers = 'localhost:9092'  # Replace with your Kafka broker's address
    topic = 'coordinates'
    num_messages = 10
    produce_messages(bootstrap_servers, topic, num_messages)
