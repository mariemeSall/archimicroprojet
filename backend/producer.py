import time
import random
import socket
from confluent_kafka import Producer
"""
running this will create test coordinates
directly to the broker running on local
"""
NUM_PARTITIONS = 2	

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {}, partition: [{}]'.format(msg.topic(), msg.partition()))

def generate_coordinate():
    # Generate random latitude and longitude
    lat = round(random.uniform(-90, 90), 6)
    lon = round(random.uniform(-180, 180), 6)

    # Get the current date and time in ISO format
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    return f'{lat}; {lon}; {current_date}'

def get_machine_partition():
    # Modify this function to return a machine-specific value for the partition
    # For example, you can use the machine's hostname, IP address, or any other criteria
    # The returned value should be an integer representing the partition number.
    # Ensure that the number is within the range of available partitions for the topic.
    return hash(socket.gethostname()) % NUM_PARTITIONS

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
    bootstrap_servers = 'localhost:9092'  # Replace with your Kafka broker's address
    topic = 'coordinates'
    num_messages = 50
    produce_messages(bootstrap_servers, topic, num_messages)