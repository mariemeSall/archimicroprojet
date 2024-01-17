import time
import random
import socket
import hashlib
from confluent_kafka import Producer
"""
running this will create test coordinates
directly to the broker running on local
"""
NUM_PARTITIONS = 10

def generate_coordinate():
    # Generate random latitude and longitude
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)

    # Get the current date and time in ISO format
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    ip_address = socket.gethostbyname(socket.gethostname())

    return f'{lat}; {lon}; {ip_address}; {current_date}'

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {}, partition: [{}]'.format(msg.topic(), msg.partition()))

def get_machine_partition():
    # Get the machine's IP address
    ip_address = socket.gethostbyname(socket.gethostname())

    # Use a hash function to generate a consistent hash value
    hash_value = int(hashlib.sha256(ip_address.encode()).hexdigest(), 16)

    # Calculate the partition based on the hash value
    partition = hash_value % NUM_PARTITIONS

    return partition

def produce_messages(bootstrap_servers, topic, num_messages):
    producer_conf = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_conf)

    for _ in range(num_messages):
        message = generate_coordinate()
        partition = get_machine_partition()
        producer.produce(topic, value=message, partition=partition, callback=delivery_report)
        time.sleep(1)

    producer.flush()

if __name__ == '__main__':
    bootstrap_servers = 'localhost:9092'  # Kafka broker's address
    topic = 'coordinates'
    num_messages = 50
    produce_messages(bootstrap_servers, topic, num_messages)